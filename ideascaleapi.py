''' Python library for interacting with the IdeaScale's API (Alpha version).

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
    
'''

__author__ = "Greg Elin (greg@greg@fotonotes.net); James Turk (jturk@sunlightfoundation.com)"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2009 Sunlight Labs"
__license__ = "BSD"

# TODO
# Get categorID working in topIdeas categoryID=2245 
# ideascale._apicall_url("ideas.getTopIdeas",params={"categoryID":2245})

# Trap for http errors - what happens if try to retrieve an url and it doesn't exist or throws other errors?

# Looks like there are some Users who are blank/no-name. How should I represent those in dictionary and in string?
#   >>> [user.name for user in ideascale.topUsers.getList()]
#   [u'ricardomigrant', u'kdtroxel', u'azaleahs', u'jbabajian', u'scyrier', u'', u'longshot9999', u'magikrider909', u'tolynette', u'sobi']
#

import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

class ApiError(Exception):
    ''' Exception for API errors '''
    pass

# results #
class ApiObject(object):
    def __init__(self, d):
        self.__dict__ = d

class Idea(ApiObject):
    def __str__(self):
        return '%s - submitted by %s' % (self.title, self.author)

class Tag(ApiObject):
    '''Creates python dictionary object and string reponse for a single Tag object from IdeaScale API.
        
        name  	    The Tag Name
        tagCount 	The # of times this tag was used
        tagVote 	The NET Cumulative value of the the Votes associated with the ideas that this tag is a part of
    '''
    def __str__(self):
        return '%s count: %s vote: %s' % (self.name,self.tagCount,self.tagVote)
        

class User(ApiObject):
    '''Creates a python dictionary object and string response for a single User object from IdeaScale API.
        Use: Pass in a single User object (e.g., from an array response of users) 
        to get back a python object that represents User.
        
        name  	User Name - If the user has updated his profile with the First/Last name then this will be returned
        ideaCount 	The # of ideas user submitted
        voteCount 	The # of votes user submitted
        url 	The Profile URL for the user
    '''
    def __str__(self):
        return ("%s %d ideas, %d votes, %s") % (self.name,self.ideaCount,self.voteCount,self.url)    


# namespaces #

class ideascale(object):

    apikey = None
    url_tpl = 'http://api.ideascale.com/akira/api/ideascale.%s?apiKey=%s&%s'
    
    @staticmethod
    def _apicall(func, params={}):
        if ideascale.apikey is None:
            raise ApiError('Missing ideascale apikey')              
        url = ideascale.url_tpl % (func, ideascale.apikey, urllib.urlencode(params))
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
        url = ideascale.url_tpl % (func, ideascale.apikey, urllib.urlencode(params))
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
        '''Returns a JSON Array of "Idea" Objects - Each with the following properties (See topIdeas)
        
            Example command line:
           >>> ideascaleapi.ideascale.topIdeas.get()
           
           A JSON Array of "Idea" Objects - Each with the following properties
           
           Property     Description
           --------     -----------
           title  	    Idea Title
           text 	    Idea Text Contents
           author 	    Idea Author - If the author has updated the profile with his First and Last name it will be returned, \
                        or else the username part of the author's email address will be returned
           URL 	        Link to the Idea
           voteCount 	Net votes count for the idea
           
           Parameters:
           categoryID (Optional)

           If a category ID is supplied, then the data is filtered for that category. To view/list the categories for this site:
           ID   Name
           2236	Making Data More Accessible 	
           2237	Making Government Operations More Open 	
           2238	Records Management 	
           2242	New Strategies and Techniques 	
           2243	New Tools and Technologies 	
           2244	Federal Advisory Committees 	
           2245	Rulemaking 	
           2246	Between Federal Agencies 	
           2247	Between Federal, State, and Local Governments 	
           2248	Public-Private Partnerships 	
           2249	Do-It-Yourself Government 	
           2250	Hiring & Recruitment 	
           2251	Performance Appraisal 	
           2252	Training and Development 	
           2253	Communications Strategies 	
           2254	Strategic Planning and Budgeting 	
           2255	Uncategorized 	
           2294	Legal & Policy Challenges
           
           title 	Idea Title
           text 	Idea Text Contents
           author 	Idea Author - If the author has updated the profile with his First and Last name \
            it will be returned, or else the username part of the author's email address will be returned
           URL 	Link to the Idea
           voteCount 	Net votes count for the idea
        '''
        @staticmethod
        def getList(**kwargs):
            response = ideascale._apicall('ideas.getTopIdeas', kwargs)
            return [Idea(idea) for idea in response['ideas']]

    class recentIdeas(object):
        '''Returns a JSON Array of "Idea" Objects - Each with the following properties (See topIdeas)
           This will return a list of All Ideas - Sorted by time (recent first)
           
           Parameters:
           catgoryID (See topIdeas for list of values)
           
           http://api.ideascale.com/akira/api/ideascale.ideas.getRecentIdeas?apiKey=YOUR_API_KEY
        '''
        @staticmethod
        def getList(**kwargs):
            response = ideascale._apicall('ideas.getRecentIdeas', kwargs)
            return [Idea(idea) for idea in response['ideas']]


    class topTags(object):
        '''A JSON Array of "Tag" Objects - Each with the following properties
        
        Property    Description
        --------    -----------
        name  	    The Tag Name
        tagCount 	The # of times this tag was used
        tagVote 	The NET Cumulative value of the the Votes associated with the ideas that this tag is a part of

        http://api.ideascale.com/akira/api/ideascale.tags.getTopTags?apiKey=YOUR_API_KEY
        This will return a list of the tags sorted by the frequency of use.
        '''
        @staticmethod
        def getList(**kwargs):
            ''' Retrive list of topTags
                
                Use:
                >>> ideascale.topTags.getList()
                >>> ["%s" % user for user in ideascale.topTags.getList()]
            '''
            response = ideascale._apicall('tags.getTopTags', kwargs)
            return [Tag(tag) for tag in response['tags']]
            

    class topUsers(object):
        '''A JSON Array of "User" Objects - Each with the following properties
        
        Property    Description
        --------    -----------
        name  	    User Name - If the user has updated his profile with the First/Last name then this will be returned
        ideaCount 	The # of ideas user submitted
        voteCount 	The # of votes user submitted
        url 	    The Profile URL for the user

        http://api.ideascale.com/akira/api/ideascale.users.getTopUsers?apiKey=YOUR_API_KEY
        This will return a list of All users (sorted by # of ideas they've contributed)
        '''
        @staticmethod
        def getList(**kwargs):
            '''Retrieve list of topUsers
            
                Use:
                >>> ideascale.topUsers.getList()
                >>> ["%s" % user for user in ideascale.topUsers.getList()]
            '''
            response = ideascale._apicall('users.getTopUsers', kwargs)
            return [User(user) for user in response['users']]
            
            
            
 