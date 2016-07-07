import json
import union

#
# Abstract Base Model
#

class BaseModel(object):
    def __init__(self, attrs=None):
        super(BaseModel, self).__init__()
        for k, v in attrs.iteritems():
            self.__setattr__(k, v)

    def __repr__(self):
        return unicode('< union.%s(%s) >' % (type(self).__name__, 'id="%s"' % self.id))

    def __str__(self):
        return self._to_json()

    def __setattr__(self, k, v=None):
        super(BaseModel, self).__setattr__(k, v)

    def _to_json(cls):
        filtered = dict((k, v) for k, v in cls.__dict__.items()
                               if not k.startswith('_') and getattr(cls, k) is not None)
        return json.dumps(filtered, sort_keys=True, indent=4)

    @classmethod
    def all(cls):
        client = union.UnionClient(cls)
        json_data = client.make_request('get')
        return client.from_json(json_data)

    @classmethod
    def get(cls, id):
        client = union.UnionClient(cls)
        json_data = client.make_request('get', params={'id': id})
        return client.from_json(json_data)


    @classmethod
    def save(cls, params):
        client = union.UnionClient(cls)

        # Update
        if 'id' in params.keys():
            id = params.pop('id')
            json_data = client.make_request('post', params={'id': id}, post_data=params)
            return union.from_json(json_data)

        # Create
        json_data = client.make_request('post', post_data=params)
        return union.from_json(json_data)


#
# Union Object Models
#

class Customer(BaseModel):
    pass

# class Vendor(BaseModel):
#     pass

# class Sale(BaseModel):
#     pass

# class SaleItem(BaseModel):
#     pass

# class Invoice(BaseModel):
#     pass

# class Bill(BaseModel):
#     pass
