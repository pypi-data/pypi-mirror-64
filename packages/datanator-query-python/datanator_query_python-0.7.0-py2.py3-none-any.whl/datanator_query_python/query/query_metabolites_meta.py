from datanator_query_python.util import mongo_util, chem_util, file_util
from . import query_nosql
import numpy as np
from pymongo.collation import Collation, CollationStrength


class QueryMetabolitesMeta(query_nosql.DataQuery):
    '''Queries specific to metabolites_meta collection
    '''

    def __init__(self, cache_dirname=None, MongoDB=None, replicaSet=None, db=None,
                 collection_str='metabolites_meta', verbose=False, max_entries=float('inf'), username=None,
                 password=None, authSource='admin', readPreference='nearest'):
        self.collection_str = collection_str
        self.verbose = verbose
        super().__init__(cache_dirname=cache_dirname, MongoDB=MongoDB,
                        replicaSet=replicaSet, db=db,
                        verbose=verbose, max_entries=max_entries, username=username,
                        password=password, authSource=authSource,
                        readPreference=readPreference)
        self.client, self.db_obj, self.collection = self.con_db(
            self.collection_str)
        self.e_client, self.e_db_obj, self.e_collection = self.con_db('ecmdb')
        self.y_client, self.y_db_obj, self.y_collection = self.con_db('ymdb')        
        self.file_manager = file_util.FileUtil()
        self.chem_manager = chem_util.ChemUtil()
        self.collation = Collation(locale='en', strength=CollationStrength.SECONDARY)

    def get_metabolite_synonyms(self, compounds):
        ''' Find synonyms of a compound

            Args:
                compound (list): name(s) of the compound e.g. "ATP", ["ATP", "Oxygen", ...]

            Returns:
                synonyms: dictionary of synonyms of the compounds
                        {'ATP': [], 'Oxygen': [], ...}
                rxns: dictionary of rxns in which each compound is found
                    {'ATP': [12345,45678,...], 'Oxygen': [...], ...}
        '''
        synonyms = {}
        rxns = {}

        def find_synonyms_of_str(c):
            if len(c) != 0:
                query = {'synonyms': c}
                projection = {'synonyms': 1, '_id': -1, 'kinlaw_id': 1}
                collation = {'locale': 'en', 'strength': 2}
                doc = self.collection.find_one(
                    filter=query, projection=projection, collation=collation)
                synonym = {}
                rxn = {}
                try:
                    synonym[c] = doc['synonyms']
                    rxn[c] = doc['kinlaw_id']
                except TypeError as e:
                    synonym[c] = (c + ' does not exist in ' +
                                  self.collection_str)
                    rxn[c] = (c + ' does not exist in ' + self.collection_str)
                return rxn, synonym
            else:
                return ({'reactions': None}, {'synonyms': None})

        if len(compounds) == 0:
            return ({'reactions': None}, {'synonyms': None})
        elif isinstance(compounds, str):
            rxn, syn = find_synonyms_of_str(compounds)
            synonyms.update(syn)
            rxns.update(rxn)
        else:
            for c in compounds:
                rxn, syn = find_synonyms_of_str(c)
                synonyms.update(syn)
                rxns.update(rxn)
        return rxns, synonyms

    def get_metabolite_inchi(self, compounds):
        '''Given a list of compound name(s) Return the corrensponding inchi string

            Args:
                compounds: list of compounds
                ['ATP', '2-Ketobutanoate']

            Returns:
                ['....', 'InChI=1S/C4H6O3/c1-2-3(5)4(6)7/...']
        '''
        inchi = []
        projection = {'_id': 0, 'inchi': 1, 'm2m_id': 1, 'ymdb_id': 1}
        collation = {'locale': 'en', 'strength': 2}
        for compound in compounds:
            cursor = self.collection.find_one({'$or': [{'synonyms': compound},
                                                       {'name': compound}]},
                                              projection=projection, collation=collation)
            if cursor is None:
                inchi.append(
                    {"inchi": 'No inchi found.', "m2m_id": 'No ECMDB record found.',
                    "ymdb_id": 'No YMDB record found.'})
            else:                
                inchi.append(
                    {"inchi": cursor['inchi'], "m2m_id": cursor.get('m2m_id', None),
                    "ymdb_id": cursor.get('ymdb_id', None)})
        return inchi

    def get_ids_from_hash(self, hashed_inchi):
        ''' Given a hashed inchi string, find its
            corresponding m2m_id and/or ymdb_id
            Args:
                hashed_inchi (`obj`: str): string of hashed inchi
            Returns:
                result (`obj`: dict): dictionary of ids and their keys
                    {'m2m_id': ..., 'ymdb_id': ...}
        '''
        query = {'InChI_Key': hashed_inchi}
        projection = {'_id': 0}
        doc = self.collection.find_one(filter=query, projection=projection)
        result = {}
        result['m2m_id'] = doc.get('m2m_id', None)
        result['ymdb_id'] = doc.get('ymdb_id', None)

        return result

    def get_ids_from_hashes(self, hashed_inchi):
        ''' Given a list of hashed inchi string, find their
            corresponding m2m_id and/or ymdb_id
            Args:
                hashed_inchi (`obj`: list of `obj`: str): list of hashed inchi
            Returns:
                result (`obj`: list of `obj`: dict): dictionary of ids and their keys
                    [{'m2m_id': ..., 'ymdb_id': ..., 'InChI_Key': ...}, {}, ..]
        '''
        query = {'InChI_Key': {'$in': hashed_inchi}}
        projection = {'m2m_id': 1, 'ymdb_id': 1, 'InChI_Key': 1}
        docs = self.collection.find(filter=query, projection=projection)
        result = []
        if docs is None: 
            return result
        else:
            for doc in docs:
                dic = {}
                dic['m2m_id'] = doc.get('m2m_id', None)
                dic['ymdb_id'] = doc.get('ymdb_id', None)
                dic['InChI_Key'] = doc.get('InChI_Key', None)
                result.append(dic)
            return result

    def get_metabolite_hashed_inchi(self, compounds):
        ''' Given a list of compound name(s)
            Return the corresponding hashed inchi string
            Args:
                compounds: ['ATP', '2-Ketobutanoate']
            Return:
                hashed_inchi: ['3e23df....', '7666ffa....']
        '''
        hashed_inchi = []
        projection = {'_id': 0, 'InChI_Key': 1}
        collation = {'locale': 'en', 'strength': 2}
        for compound in compounds:
            cursor = self.collection.find_one({'$or': [{'synonyms': compound},
                                                        {'name': compound}]},
                                              projection=projection, collation=collation)
            if cursor is None:
                hashed_inchi.append('No inchi key found.')
            else:
                hashed_inchi.append(cursor['InChI_Key'])
        return hashed_inchi

    def get_metabolite_name_by_hash(self, compounds):
        ''' Given a list of hashed inchi, 
            return a list of name (one of the synonyms)
            for each compound
            Args:
                compounds: list of compounds in inchikey format
            Return:
                result: list of names
                    [name, name, name]
        '''
        result = []
        projection = {'_id': 0, 'synonyms': 1}
        collation = {'locale': 'en', 'strength': 2}
        for compound in compounds:
            cursor = self.collection.find_one({'InChI_Key': compound},
                                              projection=projection)
            if cursor is None:
                result.append(['None'])
                continue
            if not isinstance(cursor['synonyms'], list):
                cursor['synonyms'] = [cursor['synonyms']]
            result.append(cursor.get('synonyms', ['None']))
            # except TypeError:
            #     result.append(['None'])
        return [x[-1] for x in result]

    def get_metabolite_similar_compounds(self, compounds, num=0, threshold=0):
        ''' Given a list of compound names
            Return the top num number of similar compounds
            with tanimoto score above threshold values
            Args:
                compounds: list of compound names
                num: number of similar compounds to return
                threshold: threshold tanimoto coefficient value
                return_format: return dictionary key format, either
                                hashed inchi or name
            Return:
                result: list of similar compounds and their tanimoto score
                [ {'compound1': score, 'compound2': score, ... 'compound_num': score},
                  {'compound1': score, 'compound2': score, ... 'compound_num': score}, ...]
                    compound(1 - n) will be in name format
                raw: list of similar compounds and their tanimoto score
                [ {'compound1': score, 'compound2': score, ... 'compound_num': score},
                  {'compound1': score, 'compound2': score, ... 'compound_num': score}, ...]
                    compound(1 - n) will be in hashed_inchi format
        '''
        result = []
        raw = []
        hashed_inchi = self.get_metabolite_hashed_inchi(compounds)
        projection = {'_id': 0, 'similar_compounds': 1}

        for item in hashed_inchi:
            cursor = self.collection.find_one(filter={'InChI_Key': item},
                                              projection=projection)
            compounds = cursor['similar_compounds']
            scores = [list(dic.values()) for dic in compounds]
            scores = self.file_manager.unpack_list(scores)
            hashes = [list(dic.keys()) for dic in compounds]
            hashes = self.file_manager.unpack_list(hashes)
            names = self.get_metabolite_name_by_hash(hashes)
            # convert to numpy object for faster calculations
            scores_np = np.asarray(scores)
            indices = np.nonzero(scores_np >= threshold)
            size = indices[0].size
            if size == 0:
                raw.append({'raw': -1})
                result.append({'result': -1})
            elif 0 < size < num:
                first_size = compounds[:size]
                raw = first_size
                replaced = self.file_manager.make_dict(names[:size], scores[:size])
                result.append(replaced)
            else:
                first_num = compounds[:num]
                raw = first_num
                replaced = self.file_manager.make_dict(names[:num], scores[:num])
                result.append(replaced)

        return raw, result

    def get_unique_metabolites(self):
        """Get number of unique metabolites.

        Return:
            (:obj:`int`): number of unique metabolites.
        """
        return len(self.collection.distinct('InChI_Key', collation=self.collation))

    def get_metabolites_meta(self, inchi_key):
        """Get metabolite's meta information given inchi_key.

        Args:
            (:obj:`str`): InChI Key of metabolites

        Return:
            (:obj:`dict`): meta information object.
        """
        projection = {'_id': 0, 'reaction_participants': 0, 'similar_compounds': 0}
        query = {'InChI_Key': inchi_key}
        doc = self.collection.find_one(filter=query, projection=projection, collation=self.collation)
        if doc is None:
            return {}
        else:
            return doc

    def get_eymeta(self, inchi_key):
        """Get meta info from ECMDB or YMDB
        
        Args:
            inchi_key (:obj:`str`): inchikey of metabolite molecule.

        Return:
            (:obj:`Obj`): meta information.
        """
        projection = {'_id': 0, 'concentrations': 0}
        query = {'inchikey': inchi_key}
        doc = self.e_collection.find_one(filter=query, projection=projection, collation=self.collation)
        if doc is not None:
            return doc
        else:
            doc = self.y_collection.find_one(filter=query, projection=projection, collation=self.collation)
            return doc