from datanator_query_python.util import mongo_util, chem_util, file_util
from . import query_nosql
import json

class QuerySabio(query_nosql.DataQuery):
    '''Queries specific to sabio_rk collection
    '''

    def __init__(self, cache_dirname=None, MongoDB=None, replicaSet=None, db='datanator',
                 collection_str='sabio_rk', verbose=False, max_entries=float('inf'), username=None,
                 password=None, authSource='admin'):
        self.max_entries = max_entries
        super(query_nosql.DataQuery, self).__init__(cache_dirname=cache_dirname, MongoDB=MongoDB,
                                        replicaSet=replicaSet, db=db,
                                        verbose=verbose, max_entries=max_entries, username=username,
                                        password=password, authSource=authSource)
        self.chem_manager = chem_util.ChemUtil()
        self.file_manager = file_util.FileUtil()
        self.client, self.db_obj, self.collection = self.con_db(collection_str)

    def get_reaction_doc(self, kinlaw_id):
        '''
            Find a document on reaction with the kinlaw_id
            Args:
                kinlaw_id (:obj:`list` of :obj:`int`) list of kinlaw_id to search for
            Returns:
                result (:obj:`list` of :obj:`dict`): list of docs
        '''
        projection = {'_id': 0}
        query = {'kinlaw_id': {'$in': kinlaw_id}}
        result = []
        docs = self.collection.find(filter=query, projection=projection)
        for doc in docs:
            to_append = json.dumps(doc, indent=4, sort_keys=True, default=str)
            result.append(json.loads(to_append))
        return result

    def find_reaction_participants(self, kinlaw_id):
        ''' Find the reaction participants defined in sabio_rk using kinetic law id
        
            Args:
                kinlaw_id (:obj:`list` of :obj:`int`) list of kinlaw_id to search for

            Return:
                rxns (:obj:`list` of :obj:`dict`) list of dictionaries containing names of reaction participants
                [{'substrates': [], 'products': [] }, ... {} ]
        '''
        projection = {'products': 1, 'reactants': 1, '_id': 0, 'kinlaw_id':1}
        if isinstance(kinlaw_id, list):
            query = {'kinlaw_id': {'$in': kinlaw_id}}
        else:
            query = {'kinlaw_id': kinlaw_id}
        docs = self.collection.find(filter=query, projection=projection)
        rxns = []
        i = 0
        for doc in docs:
            if i == self.max_entries:
                break
            if i % 10 == 0:
                print('Finding reaction participants for kinlaw_id {} ...'.format(
                    doc['kinlaw_id']))

            substrates = self.file_manager.get_val_from_dict_list(doc.get('reactants',), 'name')
            products = self.file_manager.get_val_from_dict_list(doc.get('products',), 'name')

            rxn = {'substrates': substrates, 'products': products}

            rxns.append(rxn)
            i += 1

        return rxns

    def get_kinlawid_by_inchi(self, hashed_inchi):
        ''' Find the kinlaw_id defined in sabio_rk using 
            rxn participants' inchi string
            Args:
                inchi (:obj:`list` of :obj:`str`): list of inchi, all in one rxn
            Return:
                rxns (:obj:`list` of :obj:`int`): list of kinlaw_ids that satisfy the condition
                [id0, id1, id2,...,  ]
        '''
        # hashed_inchi = [self.chem_manager.inchi_to_inchikey(s)
        #                 for s in inchi]
        substrate = 'reactants.structures.InChI_Key'
        product = 'products.structures.InChI_Key'
        projection = {'kinlaw_id': 1}

        id_tally = []
        for inchi in hashed_inchi:
            ids = []
            query = {'$or': [{substrate: inchi}, {product: inchi}]}
            cursor = self.collection.find(filter=query, projection=projection)
            for doc in cursor:
                ids.append(doc['kinlaw_id'])
            id_tally.append(ids)

        return list(set(id_tally[0]).intersection(*id_tally))

    def get_kinlawid_by_rxn(self, substrates, products):
        ''' Find the kinlaw_id defined in sabio_rk using 
            rxn participants' inchi string

            Args:
                substrates: list of substrates' inchi
                products: list of products' inchi

            Return:
                rxns: list of kinlaw_ids that satisfy the condition
                [id0, id1, id2,...,  ]
        '''

        def get_kinlawid(hashed_inchi, side='substrate'):
            ''' Find the kinlaw_id defined in sabio_rk using 
                rxn participants' inchi string

                Args:
                    inchi: list of inchi, all in one rxn, on one side

                Return:
                    rxns: list of kinlaw_ids that satisfy the condition
                    [id0, id1, id2,...,  ]
            '''

            substrate = 'reactants.structures.InChI_Key'
            product = 'products.structures.InChI_Key'
            projection = {'kinlaw_id': 1, '_id': 0}

            id_tally = []
            if side == 'substrate':
                for inchi in hashed_inchi:
                    ids = []
                    query = {substrate: inchi}
                    cursor = self.collection.find(
                        filter=query, projection=projection)
                    for doc in cursor:
                        ids.append(doc['kinlaw_id'])
                    id_tally.append(ids)

                return list(set(id_tally[0]).intersection(*id_tally))
            else:

                for inchi in hashed_inchi:
                    ids = []
                    query = {product: inchi}
                    cursor = self.collection.find(
                        filter=query, projection=projection)
                    for doc in cursor:
                        ids.append(doc['kinlaw_id'])
                    id_tally.append(ids)

                return list(set(id_tally[0]).intersection(*id_tally))

        sub_id = get_kinlawid(substrates, side='substrate')
        pro_id = get_kinlawid(products, side='product')
        result = list(set(sub_id) & set(pro_id))

        return result

    def get_kinlawid_by_name(self, substrates, products):
        ''' Get kinlaw_id from substrates and products, all in one reaction

            Args:
                substrates: (:obj:`list` of :obj:`str`): list of substrate names
                products: (:obj:`list` of :obj:`str`): list of product names

            Returns:
                result: (:obj:`list` of :obj:`str`): list of compound names
        '''
        collation = {'locale': 'en', 'strength': 2}
        projection = {'_id': 0, 'products': 1, 'reactants': 1, 'kinlaw_id': 1}

        def get_kinlawid(compounds, side='substrate'):
            ''' Find the kinlaw_id defined in sabio_rk using 
                rxn participants' name

                Args:
                    compounds (:obj:`list` of :obj:`str`): compound names all in one rxn, on one side
                    side (:obj:`str`): left side or right side of the rxn
                    
                Return:
                    rxns: list of kinlaw_ids that satisfy the condition
                    [id0, id1, id2,...,  ]
            '''
            substrates = 'reactants.name'
            products = 'products.name'
            projection = {'kinlaw_id': 1, '_id': 0}

            id_tally = []
            if side == 'substrate':
                for name in compounds:
                    ids = []
                    query = {substrates: name}
                    cursor = self.collection.find(
                        filter=query, projection=projection, collation=collation)
                    for doc in cursor:
                        ids.append(doc['kinlaw_id'])
                    id_tally.append(ids)

                return list(set(id_tally[0]).intersection(*id_tally))
            else:

                for name in compounds:
                    ids = []
                    query = {products: name}
                    cursor = self.collection.find(
                        filter=query, projection=projection, collation=collation)
                    for doc in cursor:
                        ids.append(doc['kinlaw_id'])
                    id_tally.append(ids)

                return list(set(id_tally[0]).intersection(*id_tally))

        if substrates == None:
            sub_id = self.collection.distinct('kinlaw_id')
        else:
            sub_id = get_kinlawid(substrates, side='substrate')

        if products == None:
            pro_id = self.collection.distinct('kinlaw_id')
        else:
            pro_id = get_kinlawid(products, side='product')
            
        result = list(set(sub_id) & set(pro_id))

        return result

    def get_kinlaw_by_environment(self, taxon=None, taxon_wildtype=None, ph_range=None, temp_range=None,
                          name_space=None, observed_type=None, projection={'_id': 0}):
        """get kinlaw info based on experimental conditions
        
        Args:
            taxon (:obj:`list`, optional): list of ncbi taxon id
            taxon_wildtype (:obj:`list` of :obj:`bool`, optional): True indicates wildtype and False indicates mutant
            ph_range (:obj:`list`, optional): range of pH
            temp_range (:obj:`list`, optional): range of temperature
            name_space (:obj:`dict`, optional): cross_reference key/value pair, i.e. {'ec-code': '3.4.21.62'}
            observed_type (:obj:`list`, optional): possible values for parameters.observed_type
            projection (:obj:`dict`, optional): mongodb query result projection

        Returns:
            (list): list of kinetic laws that meet the constraints 
        """
        all_constraints = []
        if taxon:
            all_constraints.append({'taxon': {'$in': taxon}})
        if taxon_wildtype:    
            all_constraints.append({'taxon_wildtype': {'$in': taxon_wildtype}})
        if ph_range:
            all_constraints.append({'ph': {'$gte': ph_range[0], '$lte': ph_range[1]}})
        if temp_range:    
            all_constraints.append({'temperature': {'$gte': temp_range[0], '$lte': temp_range[1]}})
        if name_space:
            key = list(name_space.keys())[0]
            val = list(name_space.values())[0]
            field = 'cross_references' + '.' + key
            all_constraints.append({field: val})
        if observed_type:
            all_constraints.append({'parameters.observed_type': {'$in': observed_type}})
        
        query = {'$and': all_constraints}
        docs = self.collection.find(filter=query, projection=projection)
        result = []
        for doc in docs:
            result.append(doc)
        
        return result

    def get_subunit_by_id(self, _id):
        """Get protein subunit information by kinlaw_id.
        
        Args:
            _id (:obj:`int`): kinlaw_id.

        Return:
            (:obj:`str`): uniprot_id.
        """
        false = 'No subunit information.'
        projection = {'enzyme': 1, '_id': 0}
        doc = self.collection.find_one({'kinlaw_id': _id}, projection=projection)
        enzyme = doc['enzyme']
        if enzyme != [] and enzyme is not None:
            subunits = enzyme[0].get('subunits')
            if subunits != [] and subunits is not None:
                uniprot_id = subunits[0].get('uniprot', false)
                return uniprot_id
            else:
                return false
        else:
            return false
