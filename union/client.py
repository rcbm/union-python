'''
TODO:

More models
 - Saving
 - Deleting

Testing:
 - Nested models
 - Client tests
 - Model actions

Readme
Examples

Update API Docs
  - New token auth
  - Ensure all params are accounted for
  - Add taxes
  - Remove Address if in docs
'''

import json
import requests
import union


#
# Union Errors
#

class UnionError(Exception):
    pass

class APIError(UnionError):
    pass

class AuthenticationError(UnionError):
    pass

class ValidationError(UnionError):
    pass


#
# Union API Client
#

class UnionClient(object):
    MODEL_MAP = [
            {'model': union.Customer, 'name': 'customer', 'plural': 'customers'},
    ]

    def __init__(self, model=None):
        self.content_type =  'application/json'
        self.api_key =       union.api_key
        self.host =          union.host
        self.api_version =   union.api_version
        self.api_namespace = union.api_namespace
        self.protocol =      union.protocol
        self.model =         model
        self.params =        None
        self.response =      None

    @property
    def _model_path_name(self):
        if self.model:
            if isinstance(self.model, type):
                class_name = self.model.__name__.lower()
            else:
                class_name = self.model.__class__.__name__.lower()

            return '/%ss' % class_name

    @property
    def _url(self):
        url = "%s://%s%s" % (self.protocol, self.host, self._model_path_name)
        if self.params:
            if 'id' in self.params.keys():
                id_param = self.params.pop('id')
                url += '/%s' % id_param
            for k, v in self.params.iteritems():
                url += '&%s=%s' % (k, v)

        return url

    @property
    def _headers(self):
        return {'Accept': 'application/json',
                'Authorization': 'Token %s' % (self.api_key,)}

    @property
    def _is_valid(self):
        return True if (200 <= self.response.status_code < 300) else False

    def _look_up_model_name(self, name_type, name):
        results = [x for x in self.MODEL_MAP if x[name_type] == name.lower()]
        if results:
            return results[0]['model']

    def _get_model_from_name(self, name):
        if not isinstance(name, unicode):
            return name

        model = self._look_up_model_name('name', name)
        return model or self._look_up_model_name('plural', name)

    def from_json(self, json_data):
        '''
        Converts json response to one or more Union objects
        '''
        for k, v in json_data.iteritems():
            model = self._get_model_from_name(k)

            if isinstance(v, list):
                return [self.from_json({model: obj}) for obj in v]
            elif isinstance(v, dict) and not isinstance(v, union.BaseModel):
                return model(v)

            return json_data

    def make_request(self, action, body=None, params=None, post_data=None):
        '''
        Fire request to API and validate, parse, and return the response
        '''
        self.params = params
        url = self._url
        headers = self._headers
        action = action.lower()

        if action is not 'get':
            headers = dict(headers, **{'Content-Type': 'application/json'})

        try:
            self.response = requests.request(action, url, headers=headers, data=post_data)
        except Exception as e:
            raise APIError("There was an error communicating with Union: %s" % e)

        if not self._is_valid:
            raise ValidationError("The Union response returned an error: %s" % self.response.content)

        return json.loads(self.response.content)
