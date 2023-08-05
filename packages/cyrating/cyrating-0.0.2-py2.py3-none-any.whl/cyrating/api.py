# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
import configparser
import jwt
import arrow
import json

PATH_MASTER_TOKEN = "./cyrating.ini"
APP_URL = "https://api.cyrating.com"
COMPANY_ENDPOINT = '/company'
CLIENT_ENDPOINT = '/client'
CERTIFICATE_ENDPOINT = '/certificate'
ASSETS_ENDPOINT = '/assets'
TAGS_ENDPOINT = '/tags'


def jsonFilter(dic):
  if isinstance(dic, list):
    return dic
  res = {}
  for key in dic.keys():
    if not key.startswith('_'):
      res[key] = dic[key]
  return res


class Cyrating(object):
  def __init__(self, **kwargs):
    """ Init a Cyrating context """

    self._requests = requests.Session()
    self._requests.mount('', HTTPAdapter(max_retries=5))

    self.__app_url__ = 'http://127.0.0.1:5000' if 'debug' in kwargs else APP_URL
    self.__access_token__ = kwargs.get('token') if 'token' in kwargs else self.get_personal_token()
    decoded_atoken = jwt.decode(self.__access_token__, verify=False)
    self.__headers__ = {"Content-Type": "application/json",
                        "Authorization": "Bearer " + self.__access_token__}
    self.__current_user_id__ = decoded_atoken['sub']

    (tmp, self.__current_client_id__, self.__current_role) = decoded_atoken['ccs'].split(':')
    self.client(self.__current_client_id__)
    print("# Access Token for ", self.__app_url__, "expires at",
          arrow.get(decoded_atoken['exp']))

  def get_personal_token(self):
    """ Read personal token from configuration file """

    config = configparser.ConfigParser()
    config.read(PATH_MASTER_TOKEN)
    return config['cyrating']['token']

  def get(self, endpoint, id, extraHttpRequestParams=None):
    url = self.__app_url__ + endpoint + '/' + id
    res = self._requests.get(url,
                             params=extraHttpRequestParams,
                             headers=self.__headers__)
    if res.ok:
      jData = json.loads(res.content)
      return jData
    return None

  def post(self, endpoint, obj, extraHttpRequestParams=None):
    res = self._requests.post(self.__app_url__ + endpoint,
                              json.dumps(obj),
                              params=extraHttpRequestParams,
                              headers=self.__headers__)
    print(res.content, json.dumps(obj))
    if res.ok:
      jData = json.loads(res.content)
      return jData

  def patch(self, obj, extraHttpRequestParams=None):
    headers = self.__headers__.copy()
    headers.update({"If-Match": obj['_etag']})

    print('PATCH', json.dumps(jsonFilter(obj)))

    res = self._requests.patch(self.__app_url__ + '/' + obj['_links']['self']['href'],
                               json.dumps(jsonFilter(obj)),
                               headers=headers,
                               params=extraHttpRequestParams,
                               stream=False)
    if res.ok:
      jData = json.loads(res.content)
      return jData
    return None

  def find_one(self, endpoint, extraHttpRequestParams=None):
    queryParameters = {'page': 1, 'max_results': 100}

    if extraHttpRequestParams:
      queryParameters.update(extraHttpRequestParams)

    res = self._requests.get(self.__app_url__ + endpoint,
                             params=queryParameters,
                             headers=self.__headers__)
    if res.ok:
      jData = json.loads(res.content)
      assert len(jData['_items']) >= 0, 'Error multiple instance of {} in {}'.format(extraHttpRequestParams, endpoint)
      if len(jData['_items']) == 0:
        return None
      return jData['_items'][0]
    return None

  def client(self, clientid):
    """ Retrieve client obj from API """

    answer = self.get(CLIENT_ENDPOINT, clientid)
    if not answer:
      self.__current_client__ = None
      return
    self.__current_client__ = dict(
        name=answer['name'] if 'name' in answer else None,
        company_id=answer['companyID'] if 'companyID' in answer else None,
        entities_id=answer['entitiesID'] if 'entitiesID' in answer else None,
        suppliers_id=answer['suppliersID'] if 'suppliersID' in answer else None,
    )

  def get_company(self, id):
    """ Retrieve company obj from API """

    return self.get(COMPANY_ENDPOINT, id)

  def certificate(self, company, filename=None):
    """ Get certificate of a company """

    httpParams = dict(
        clientid=self.__current_client_id__,
        orgid=company['_id']
    )
    answer = self._requests.get(self.__app_url__ + CERTIFICATE_ENDPOINT,
                                params=httpParams,
                                headers=self.__headers__)

    if not answer.ok:
      raise Exception('Failed to retreive certificate for {}'.format(company['name']))

    if filename:
      try:
        with open(filename, 'wb') as f:
          f.write(answer.content)
      except Exception as e:
        raise Exception('Failed to save {}: {}'.format(filename, e))
    else:
      return answer.content

  def main_company(self):
    """ Get main company """

    return self.get_company(self.__current_client__['company_id'])

  def entities(self):
    """ Get list of entities """

    return [self.get_company(companyid) for companyid in self.__current_client__['entitiesID']]

  def suppliers(self):
    """ Get list of suppliers """

    return [self.get_company(companyid) for companyid in self.__current_client__['suppliersID']]

  def assets(self, company):
    """ Get list of assets of a company """

    # const assets = this.apiService.findAll(environment.API_ENDPOINT_ASSETS, 1, 100,  {'where': {'company': company._id}})
    filter = {'where': json.dumps({'company': company['_id']})}
    return self.find_one(ASSETS_ENDPOINT, filter)

  def domains(self, company):
    """ Get list of domains associated to a company """

    assets = self.assets(company)
    if assets is not None:
      return [item['label'] for item in assets['nodes'] if item['type'] == 'domain']
    return None

  def set_tags(self, domainname, tags):
    if domainname is None:
      print('* Domain name is None')
      return
    if not isinstance(tags, list):
      print('* Tags is not an array')
      return
    tags_obj = self.get(TAGS_ENDPOINT, domainname)
    if not tags_obj:
      self.post(TAGS_ENDPOINT, {'domainname': domainname, 'tags': tags})
    else:
      tags_obj.update({'tags': tags})
      self.patch(tags_obj)
