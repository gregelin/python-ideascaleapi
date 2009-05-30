""" Python library for interacting with the IdeaScale's API (Alpha version).

    The Sunlight Labs API (http://services.sunlightlabs.com/api/) provides basic
    legislator data, conversion between ids, and zipcode-district lookups.
    

    Current method calls available:
    Idea related Methods:
        ideascale.ideas.getTopIdeas
        ideascale.ideas.getRecentIdeas
    
    Tag Related Methods:
        ideascale.tags.getTopTags

    User Related Methods:
        ideascale.users.getTopUsers

    
    
    References
    http://opengov.ideascale.com/akira/ideascaleStatic.do?mode=api
    http://ideas.ideascale.com/akira/ideafactory.do?discussionID=12038
    
    Changes from original python-sunlightlabs
    
    5.30.2009
        - Changed SunlightApiObject to ApiObject
        - Changed SunlightApiError to ApiError
        - Changed class 'sunlight' to 'ideascale'
        - Added some simple test methods
        - Repointed url template to ideascale url instead of Sunlight Labs
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

class TopIdeas(ApiObject):
    def __str__(self):
        return [idea for idea in self.ideas]
#        return '%s. %s %s (%s-%s)' % (self.title, fname, self.lastname, self.party, self.state)


# namespaces #

class ideascale(object):

    apikey = None

    @staticmethod
    def _apicall(func, params={}):
        if ideascale.apikey is None:
            raise ApiError('Missing ideascale apikey')

        url = 'http://api.ideascale.com/akira/api/ideascale.%s?apiKey=%s&%s' % \
              (func, ideascale.apikey, urllib.urlencode(params))
        try:
            response = urllib2.urlopen(url).read()
            return json.loads(response)['response']
        except urllib2.HTTPError, e:
            raise ApiError(e.read())
        except (ValueError, KeyError), e:
            raise ApiError('Invalid Response')
    
    @staticmethod
    def _apicall_url(func, params={}):
        if ideascale.apikey is None:
            raise ApiError('Missing ideascale apikey')

        url = 'http://api.ideascale.com/akira/api/ideascale.%s?apiKey=%s&%s' % \
              (func, ideascale.apikey, urllib.urlencode(params))
        return url
    
    @staticmethod
    def test():
        return "Test OK"
        
    @staticmethod
    def get_apikey():
        if ideascale.apikey is None:
            raise ApiError('Missing ideascale apikey')
        else:
            return ideascale.apikey
        
    class topIdeas(object):
        @staticmethod
        def get(**kwargs):
            result = ideascale._apicall('getTopIdeas', kwargs)
            return [TopIdeas(response['ideas']) for response in results]


    class recentIdeas(object):
        @staticmethod
        def get(**kwargs):
            result = ideascale._apicall('ideas.getRecentIdeas', kwargs)
            return [response['ideas'] for response in results]


 