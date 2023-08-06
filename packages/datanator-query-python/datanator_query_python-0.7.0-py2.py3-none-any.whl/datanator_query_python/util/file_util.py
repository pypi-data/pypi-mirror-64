from itertools import chain
from bson import ObjectId
import json

class FileUtil:

    def extract_values(self, obj, key):
        """Pull all values of specified key from nested JSON.
        """
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        results = extract(obj, arr, key)

        return results

    def get_val_from_dict_list(self, dict_list, key):
        '''
            Get values for key from a list of dictionaries
            Args:
                dict_list (:obj:`list` of :obj:`dict`): list of dictionary 
                                                        to query
                key (:obj:`str`): key for which to get the value
            Returns:
                results (:obj:`list` of :obj:): list of values
        '''
        result = []
        for dic in dict_list:
            if dic.get(key) is not None:
                 result.append(dic.get(key))
            else:
                continue
        return result


    def flatten_json(self, nested_json):
        '''
            Flatten json object with nested keys into a single level.
            e.g. 
            {a: b,                      {a: b,  
             c: [                        d: e,
                {d: e},    =>            f: g }
                {f: g}]}
            Args:
                nested_json: A nested json object.
            Returns:
                The flattened json object if successful, None otherwise.
        '''
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(nested_json)
        return out

    def unpack_list(self, _list):
        ''' Unpack sublists in a list
            Args:
                _list: a list containing sublists  e.g. [ [...], [...], ...  ]
            Return:
                result: unpacked list e.g. [ ....  ]
        '''
        return list(chain.from_iterable(_list))

    def access_dict_by_index(self, _dict, count):
        ''' Assuming dict has an order, return 
            the first num of elements in dictionary
            Args:
                _dict: { 'a':1, 'b':2, 'c':3, ... }
                count: number of items to return
            Return:
                result: a dictionary with the first count 
                        from _dict
                        {'a':1}
        '''
        result = {}
        tuples = _dict.items()
        i = 0
        for item in tuples:
            if i == count:
                continue
            result[item[0]] = item[1]
            i += 1
        return result

    def replace_dict_key(self, _dict, replacements):
        ''' Replace keys in a dictionary with the order
            in replacements e.g.,
            {'a': 0, 'b': 1, 'c': 2}, ['d', 'e', 'f'] =>
            {'d': 0, 'e': 1, 'f': 2}            
            Args:
                _dict: dictionary whose keys are to be replaced
                replacement: list of replacement keys

            Return:
                result: dictionary with replaced keys
        '''
        result = {}
        i = 0

        for k, v in _dict.items():
            result[replacements[i]] = v
            i += 1
        return result

    def search_dict_index(self, dict_list, key, value):
        '''
            Find the index of the dictionary that contains key/val
            pair within the dict_list

            Args:
                dict_list (:obj:`list` of :obj:`dict`): list of dictionaries
                key (:obj:`str`): dictionary key
                value (:obj:): dictionary value.

            Returns:
                index (:obj:`list` of :obj:`int`): list of indices.
        '''
        index = []
        for i, dic in enumerate(dict_list):
            val = dic.get(key, None)
            if val == value:
                index.append(i)
        return index

    def get_common(self, list1, list2):
        ''' Given two lists, find the closest
            common ancestor.

            Args:
                list1(:obj:`list`): [a, b, c, f, g] 
                list2(:obj:`list`): [a, b, d, e]

            Return:
                (:obj:`obj`): the closest common ancestor, in
                the above example would be b.
        '''
        ancestor = ''
        for a, b in zip(list1, list2):
            if a == b:
                ancestor = a
            else:
                return ancestor
        return ancestor

    def make_dict(self, keys, values):
        ''' Give two lists, make a list of 
            dictionaries
            Args:
                keys: [a, b, c, d, ...]
                values: [1, 2, 3, 4]
            Return:
                dic: {'a': 1, 'b': 2, 'c': 3, ...} 
        '''
        result = {}
        for k, v in zip(keys, values):
            result[k] = v
        return result

    def search_dict_list(self, dict_list, key, value=''):
        ''' Find the dictionary with 
            key/value pair in a list of dictionaries

            Args:
                dict_list (:obj:`list`): list of dictionaries
                key (:obj:`string`): key in the dictionary
                value (:obj:``): value to be matched
                                if value==None, then only search for key
            Returns:
                result (:obj:`list` of :obj:`dict`): list of dictionaries with the key/value pair
        '''
        if value:
            return list(filter(lambda search: search.get(key, None) == value, dict_list))
        else:
            result = []
            [result.append(d) for i,d in enumerate(dict_list) if key in d]
            return result

    def merge_dict(self, dicts):
        ''' Merge a list of dictionaries
            Args:
                dicts (:obj:`list` of :obj:`dict`): list of dictionaries
            Returns:
                result (:obj:`dict`): merged dictionries
        '''
        result = {}
        for d in dicts:
            for k, v in d.items(): 
                result[k] = v
        return result

    def exists_key_value_pair(self, dictionary, k, v):
        ''' Test if a key/value pair exists in dictionary
            Args:
                dict (:obj:`dict`): dictionary to be checked
                k (:obj:`str`): key to be matched
                v (:obj:``): value to be matched
            Returns:
                result (:obj:`bool`): True or False
        '''
        return k in dictionary and v == dictionary[k]

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
