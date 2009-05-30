""" Python library for interacting with the Sunlight Labs API.

    The Sunlight Labs API (http://services.sunlightlabs.com/api/) provides basic
    legislator data, conversion between ids, and zipcode-district lookups.
    
    
    Changes from original python-sunlightlabs
    
    5.30.2009
        - Changed SunlightApiObject to ApiObject
        - Changed SunlightApiError to ApiError
        - Changed class 'sunlight' to 'ideascale'
"""

__author__ = "Greg Elin (greg@greg@fotonotes.net); James Turk (jturk@sunlightfoundation.com)"
__version__ = "0.4.0"
__copyright__ = "Copyright (c) 2009 Sunlight Labs"
__license__ = "BSD"

import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

class ApiError(Exception):
    """ Exception for API errors """

# results #
class ApiObject(object):
    def __init__(self, d):
        self.__dict__ = d

class getTopIdeas(ApiObject):
    def __str__(self):
        if self.nickname:
            fname = self.nickname
        else:
            fname = self.firstname
        return '%s. %s %s (%s-%s)' % (self.title, fname, self.lastname,
                                      self.party, self.state)

class Legislator(ApiObject):
    def __str__(self):
        if self.nickname:
            fname = self.nickname
        else:
            fname = self.firstname
        return '%s. %s %s (%s-%s)' % (self.title, fname, self.lastname,
                                      self.party, self.state)


# namespaces #

class ideascale(object):

    apikey = None

    @staticmethod
    def _apicall(func, params):
        if sunlight.apikey is None:
            raise ApiError('Missing ideascale apikey')

        url = 'http://api.ideascale.com/akira/api/ideascale%s?apiKey=%s&%s' % \
              (func, ideascale.apikey, urllib.urlencode(params))
        try:
            response = urllib2.urlopen(url).read()
            return json.loads(response)['response']
        except urllib2.HTTPError, e:
            raise ApiError(e.read())
        except (ValueError, KeyError), e:
            raise ApiError('Invalid Response')

    class getTopIdeas(object):
        @staticmethod
        def get(**kwargs):
            result = sunlight._apicall('legislators.get', kwargs)['legislator']
            return Legislator(result)

        @staticmethod
        def getList(**kwargs):
            results = sunlight._apicall('legislators.getList', kwargs)
            return [Legislator(l['legislator']) for l in results['legislators']]

        @staticmethod
        def search(name, threshold=0.9, all_legislators=False):
            params =  {'name':name, 'threshold': threshold}
            if all_legislators:
                params['all_legislators'] = 1
            results = sunlight._apicall('legislators.search', params)['results']
            return [LegislatorSearchResult(r['result']) for r in results]

        @staticmethod
        def allForZip(zipcode):
            results = sunlight._apicall('legislators.allForZip', {'zip':zipcode})
            return [Legislator(l['legislator']) for l in results['legislators']]

    
    class legislators(object):
        @staticmethod
        def get(**kwargs):
            result = sunlight._apicall('legislators.get', kwargs)['legislator']
            return Legislator(result)

        @staticmethod
        def getList(**kwargs):
            results = sunlight._apicall('legislators.getList', kwargs)
            return [Legislator(l['legislator']) for l in results['legislators']]

        @staticmethod
        def search(name, threshold=0.9, all_legislators=False):
            params =  {'name':name, 'threshold': threshold}
            if all_legislators:
                params['all_legislators'] = 1
            results = sunlight._apicall('legislators.search', params)['results']
            return [LegislatorSearchResult(r['result']) for r in results]

        @staticmethod
        def allForZip(zipcode):
            results = sunlight._apicall('legislators.allForZip', {'zip':zipcode})
            return [Legislator(l['legislator']) for l in results['legislators']]


