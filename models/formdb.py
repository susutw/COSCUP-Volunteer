from pymongo.collection import ReturnDocument

from models.base import DBBase

class FormDB(DBBase):
    ''' Form Collection

    .. note::
        - ``pid``, ``uid``, ``form_case``
        - ``available`` bool to check use or not

    '''
    def __init__(self):
        super(FormDB, self).__init__('form')

    def index(self):
        ''' Index '''
        self.create_index([('case', 1), ])
        self.create_index([('pid', 1), ])

    def add_by_case(self, case, pid, uid, data):
        ''' add data by case

        :param str case: form case
        :param str pid: project id
        :param str uid: user id
        :param dict data: form data

        '''
        _data = {}
        for k in data:
            _data['data.%s' % k] = data[k]

        return self.find_one_and_update(
            {'case': case, 'pid': pid, 'uid': uid},
            {'$set': _data},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )


class FormTrafficFeeMappingDB(DBBase):
    ''' Form traffic fee mapping Collection '''
    def __init__(self):
        super(FormTrafficFeeMappingDB, self).__init__('form_traffic_fee_mapping')

    def save(self, pid, data):
        ''' Save location / fee data

        :param str pid: pid
        :param dict data: {'(location)': (fee)}

        '''
        return self.find_one_and_update(
                {'_id': pid},
                {'$set': {'data': data}},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )
