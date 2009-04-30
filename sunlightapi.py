""" Python library for interacting with the Sunlight Labs API.

    The Sunlight Labs API (http://services.sunlightlabs.com/api/) provides basic
    legislator data, conversion between ids, and zipcode-district lookups.
"""

__author__ = "James Turk (jturk@sunlightfoundation.com)"
__version__ = "0.4.0"
__copyright__ = "Copyright (c) 2009 Sunlight Labs"
__license__ = "BSD"

import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

class SunlightApiError(Exception):
    """ Exception for Sunlight API errors """

# results #
class SunlightApiObject(object):
    def __init__(self, d):
        self.__dict__ = d

class Legislator(SunlightApiObject):
    def __str__(self):
        if self.nickname:
            fname = self.nickname
        else:
            fname = self.firstname
        return '%s. %s %s (%s-%s)' % (self.title, fname, self.lastname,
                                      self.party, self.state)

class LegislatorSearchResult(SunlightApiObject):
    def __init__(self, d):
        self.legislator = Legislator(d['legislator'])
        self.score = d['score']

    def __str__(self):
        return '%s %s' % (self.score, self.legislator)

class Committee(SunlightApiObject):
    def __init__(self, d):
        self.__dict__ = d
        self.subcommittees = [Committee(sc['committee']) for sc in getattr(self, 'subcommittees', [])]
        self.members = [Legislator(m['legislator']) for m in getattr(self, 'members', [])]

    def __str__(self):
        return '%s' % (self.name)

class District(SunlightApiObject):
    def __str__(self):
        return '%s-%s' % (self.state, self.number)

class Lobbyist(SunlightApiObject):
    def __str__(self):
        return '%s %s' % (self.firstname, self.lastname)

class Issue(SunlightApiObject):
    def __str__(self):
        return '%s (%s)' % (self.code, self.specific_issue)

class Filing(SunlightApiObject):
    def __init__(self, d):
        self.__dict__ = d
        self.lobbyists = [Lobbyist(l['lobbyist']) for l in self.lobbyists]
        self.issues = [Issue(i['issue']) for i in self.issues]

    def __str__(self):
        return '%s - %s for %s' % (self.filing_id, self.registrant_name,
                                   self.client_name)

class FilingSearchResult(SunlightApiObject):
    def __init__(self, d):
        self.__dict__ = d['lobbyist']
        self.score = d['score']

    def __str__(self):
        return '%s %s %s (%s)' % (self.score, self.firstname, self.lastname,
                                  self.registrant_name)

# namespaces #

class sunlight(object):

    apikey = None

    @staticmethod
    def _apicall(func, params):
        if sunlight.apikey is None:
            raise SunlightApiError('Missing sunlight apikey')

        url = 'http://services.sunlightlabs.com/api/%s.json?apikey=%s&%s' % \
              (func, sunlight.apikey, urllib.urlencode(params))
        try:
            response = urllib2.urlopen(url).read()
            return json.loads(response)['response']
        except urllib2.HTTPError, e:
            raise SunlightApiError(e.read())
        except (ValueError, KeyError), e:
            raise SunlightApiError('Invalid Response')

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
        def search(name, threshold=0.9):
            params =  {'name':name, 'threshold': threshold}
            results = sunlight._apicall('legislators.search', params)['results']
            return [LegislatorSearchResult(r['result']) for r in results]

        @staticmethod
        def allForZip(zipcode):
            results = sunlight._apicall('legislators.allForZip', {'zip':zipcode})
            return [Legislator(l['legislator']) for l in results['legislators']]

    class committees(object):
        @staticmethod
        def get(committee_id):
            results = sunlight._apicall('committees.get', {'id':committee_id})
            return Committee(results['committee'])

        @staticmethod
        def getList(chamber):
            results = sunlight._apicall('committees.getList', {'chamber':chamber})
            return [Committee(c['committee']) for c in results['committees']]

        @staticmethod
        def allForLegislator(bioguide_id):
            results = sunlight._apicall('committees.allForLegislator',
                                        {'bioguide_id': bioguide_id})
            return [Committee(c['committee']) for c in results['committees']]

    class districts(object):
        @staticmethod
        def getDistrictsFromZip(zipcode):
            results = sunlight._apicall('districts.getDistrictsFromZip', {'zip':zipcode})
            return [District(r['district']) for r in results['districts']]

        @staticmethod
        def getZipsFromDistrict(state, district):
            params = {'state':state, 'district':district}
            results = sunlight._apicall('districts.getZipsFromDistrict', params)
            return results['zips']

        @staticmethod
        def getDistrictFromLatLong(latitude, longitude):
            params = {'latitude':latitude, 'longitude':longitude}
            result = sunlight._apicall('districts.getDistrictFromLatLong', params)
            return District(result['districts'][0]['district'])

    class lobbyists(object):
        @staticmethod
        def getFiling(id):
            result = sunlight._apicall('lobbyists.getFiling', {'id':id})
            return Filing(result['filing'])

        @staticmethod
        def getFilingList(**kwargs):
            results = sunlight._apicall('lobbyists.getFilingList', kwargs)
            return [Filing(f['filing']) for f in results['filings']]

        @staticmethod
        def search(name, year=None, threshold=0.9):
            if year == None:
                import time
                year = time.strftime('%Y')
            params = {'name':name, 'year':year, 'threshold': threshold}
            results = sunlight._apicall('lobbyists.search', params)['results']
            return [FilingSearchResult(f['result']) for f in results]

    class wordlist(object):

        @staticmethod
        def _apicall(call, body=None):
            base_url = 'http://services.sunlightlabs.com/api/wordlist'
            url = '%s/%s/?apikey=%s' % (base_url, call, sunlight.apikey)
            try:
                if body:
                    data = urllib.urlencode(body)
                else:
                    data = None
                return urllib2.urlopen(url, data).read()
            except urllib2.HTTPError, e:
                raise SunlightApiError(e.read())

        @staticmethod
        def get(list_name):
            words = sunlight.wordlist._apicall(list_name)
            return words.split('~')

        @staticmethod
        def update(list_name, words):
            sunlight.wordlist._apicall(list_name, {'words': '\n'.join(words)})

        @staticmethod
        def filter_stopwords(list_name, text):
            call = '%s/filter_stopwords' % list_name
            return sunlight.wordlist._apicall(call, {'text': text})
