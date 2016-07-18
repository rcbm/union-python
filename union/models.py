import json
import union

#
# Abstract Base Model
#

class BaseModel(object):
    def __init__(self, **attrs):
        for k, v in attrs.iteritems():
            self.__setattr__(k, v)

    def __repr__(self):
        return unicode('< union.%s(%s) >' % (type(self).__name__, self))

    def __str__(self):
        return self._to_json

    def __setattr__(self, k, v=None):
        super(BaseModel, self).__setattr__(k, v)

    @property
    def _to_dict(self):
        return dict((k, v) for k, v in self.__dict__.items()
                               if not k.startswith('_') and getattr(self, k) is not None)

    @property
    def _to_json(self):
        return json.dumps(self._to_dict, sort_keys=True, indent=4)

    @classmethod
    def all(cls):
        '''
        Returns multiple Union objects
        '''
        client = union.UnionClient(cls)
        return client.make_request('get')

    @classmethod
    def get(cls, id):
        '''
        Look up one Union object
        '''
        client = union.UnionClient(cls)
        return client.make_request('get', params={'id': id})

    def save(self):
        '''
        Save an instance of a Union object
        '''
        client = union.UnionClient(self)
        params = None if not self.id else {'id': self.id}
        action = 'patch' if self.id else 'post'
        return client.make_request(action, params=params, post_data=self._to_json)


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
