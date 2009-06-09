===================
python-ideascaleapi
===================

Python library for interacting with the IdeaScale API.
(Based on Python library for interacting with Sunlight Labs API.)

The IdeaScale API provides ability to extract information from IdeaScale discussions.
IdeaScale offers a RESTful and SOAP API. This library is for the RESTful API.

(http://opengov.ideascale.com/akira/ideascaleStatic.do?mode=api)

python-ideascaleapi is a project of Greg Elin <greg@fotonotes.net>

Python-ideascaleapi is based on python-sunlightlabs project of Sunlight Labs (c) 2008.  
Written by James Turk <jturk@sunlightfoundation.com>.

All code is under a BSD-style license, see LICENSE for details.

Homepage: http://pypi.python.org/pypi/python-ideascaleapi/

Source: http://github.com/sunlightlabs/python-ideascaleapi/


Requirements
============

python >= 2.4

simplejson >= 1.8 (not required with python 2.6, will use built in json module)


Change log
============
5.30.2009
    - Changed SunlightApiObject to ApiObject
    - Changed SunlightApiError to ApiError
    - Changed class 'sunlight' to 'ideascale'
    - Added some simple test methods
    - Repointed url template to ideascale url instead of Sunlight Labs
6.5.2009
    - Added support for ideascale.tags.getTopTags 
6.9.2009
    - Added support for ideascale.users.getTopUsers
    - Documentation clean up


Installation
============
To install run

    ``python setup.py install``

which will install the bindings into python's site-packages directory.

Usage
=====

To initialize the api, all that is required is for it to be imported and for an
API key to be defined.

(If you do not have an API key visit http://opengov.ideascale.com/akira/ideascaleStatic.do?mode=api to
register for one.)

Import ``ideascale`` from ``ideascaleapi``:
    
    >>> from ideascaleapi import ideascale, ApiError
    

And set your API key:
    
    >>> ideascale.apikey = 'your ideascale-api-key'

Example:
	>>> ideascale.apikey = '413fcf72-410r-4d33-b3d0-fd0ecef4xb8d'


Python Command-line example:

	>>> from ideascaleapi import ideascale, ApiError
	>>> import simplejson as json
	>>> import urllib
	>>> ideascale.apikey = 'your-ideascale-api-key'
	>>> ideascale._apicall_url('ideas.getTopideas')
	'http://api.ideascale.com/akira/api/ideascale.ideas.getTopideas?apiKey=your-ideascale-api-key&'
	>>> ideascale._apicall('ideas.getTopIdeas')
	'{"response":{"ideas":[{"author":"longshot9999","text":"Is this issue more important...
	(long output of JSON object ....')
	>>> ideascale.topIdeas.getList()
	[<ideascaleapi.Idea object at 0x105dd90>, <ideascaleapi.Idea object at 0x1068e50>...
	...<ideascaleapi.Idea object at 0x1074590>
	
	Look at title of second idea in return list of object ideas
	>>> deascale.topIdeas.getList()[2].title
	u'A Rite of Passage?'
	>>> ideascaleapi.ideascale.topIdeas.get()[2].voteCount
	1000
	
	>>> u1 = json.loads(urllib.urlopen(u).read())


-------------
ideas methods
-------------

The ideas namespace is comprised of two methods:

    • topIdeas.getList() - get zero or more top ideas
    • recentIdeas.getList() - get zero or most recent ideas (ideascale currently returns max 50 and no pagination)

	get and getList
	---------------

	Note:  Ideascale API currently returns a maximum of 50 results. No pagination.
	
	topIdeas.getList and recentIdeas.getList methods take any number of parameters (i.e. using **kwargs)
	and return all idea that match the provided criteria.  

	
	The available parameters are:
	    * categoryID (optional); categoryID=xxxx	
		ID		Name
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

Properties of ideascale idea:

		Property	Description
		--------	-----------
		title  		Idea Title
		text 		Idea Text Contents
		author 		Idea Author - If the author has updated the profile with his First and Last name it will be returned,
		 			or else the username part of the author's email address will be returned
		URL 		Link to the Idea
		voteCount 	Net votes count for the idea

Examples:

	To retreive top ideas:
	
	>>> print ideascaleapi.ideascale.topIdeas.getList()

	To retreive top 3 ideas:
	
		>>> ["%s" % idea for idea in ideascale.topTags.getList()[0:2]]
		[u'birth certificate count: 99 vote: 0', u'transparency count: 55 vote: 0']

	To get the top ideas from Rulemaking:  ###### NOT WORKING AS OF 6/9/2009

	    >>> print ideascaleapi.ideascale.topIdeas.getList(categoryID=2245)
	    


------------
tags methods
------------

The tags namespace is comprised of one method:
	
	• topTags.getList() - get zero or more topTags

	get and getList
	---------------

	Note:  Ideascale API currently returns a maximum of 50 results. No pagination.
	
	topTags.getList method takes any number of parameters (i.e. using **kwargs)
	and return all idea that match the provided criteria.  However, ideaScale API 
	does not support any parameters at this time.

	
Properties of ideascale tag:

	Property	Description
	--------	-----------
	name  		The Tag Name
	tagCount 	The # of times this tag was used
	tagVote 	The NET Cumulative value of the the Votes associated with the ideas that this tag is a part of


-------------
users methods
-------------

The users namespace is comprised of one method:

	• topUsers.getList() - get zero or more topUsers

	get and getList
	---------------

	Note:  Ideascale API currently returns a maximum of 50 results. No pagination.
	
	topTags.getList method takes any number of parameters (i.e. using **kwargs)
	and return all idea that match the provided criteria.  However, ideaScale API 
	does not support any parameters at this time.

Properties of ideascale user:

	Property	Description
	--------	-----------
	name  		The Tag Name
	tagCount 	The # of times this tag was used
	tagVote 	The NET Cumulative value of the the Votes associated with the ideas that this tag is a part of





