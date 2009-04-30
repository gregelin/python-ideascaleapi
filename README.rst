==================
python-sunlightapi
==================

Python library for interacting with the Sunlight Labs API.

The Sunlight Labs API provides basic legislator information, district lookups,
and experimental information on lobbyists.
(http://services.sunlightlabs.com/api/)

python-sunlightapi is a project of Sunlight Labs (c) 2008.  
Written by James Turk <jturk@sunlightfoundation.com>.

All code is under a BSD-style license, see LICENSE for details.

Homepage: http://pypi.python.org/pypi/python-sunlightapi/

Source: http://github.com/sunlightlabs/python-sunlightapi/


Requirements
============

python >= 2.4

simplejson >= 1.8 (not required with python 2.6, will use built in json module)


Installation
============
To install run

    ``python setup.py install``

which will install the bindings into python's site-packages directory.

Usage
=====

To initialize the api, all that is required is for it to be imported and for an
API key to be defined.

(If you do not have an API key visit http://services.sunlightlabs.com/api/ to
register for one.)

Import ``sunlight`` from ``sunlightapi``:
    
    >>> from sunlightapi import sunlight, SunlightApiError
    
And set your API key:
    
    >>> sunlight.apikey = 'sunlight-api-key'

-------------------
legislators methods
-------------------

The legislators namespace is comprised of several functions:
    * legislators.get        - get a single legislator
    * legislators.getList    - get zero or more legislators
    * legislators.search     - fuzzy search for legislators by name
    * legislators.allForZip  - get all legislators representing a zipcode
    

get and getList
---------------
    
legislators.get and legislators.getList both take any number of parameters and
return all legislators that match the provided criteria.  These parameters are
also the ones returned in each legislator object.  

The available parameters are:
    * title
    * firstname
    * middlename
    * lastname
    * name_suffix
    * nickname
    * party
    * state
    * district
    * in_office
    * gender
    * phone
    * fax
    * website
    * webform
    * email
    * congress_office
    * bioguide_id
    * votesmart_id
    * fec_id
    * govtrack_id
    * crp_id
    * eventful_id
    * sunlight_old_id
    * congresspedia_url
    * twitter_id
    
    
To get the representative that represents NC-4:

    >>> print sunlight.legislators.get(state='NC', district='4')
    Rep. David Price (D-NC)
    
legislators.getList works much the same way, but returns a list.  It is
possible to do a more complex query, for instance
"all legislators from New York that are Republicans":

    >>> for leg in sunlight.legislators.getList(state='NY', party='R'):
    ...     print leg
    Rep. Pete King (R-NY)
    Rep. Christopher Lee (R-NY)
    Rep. John McHugh (R-NY)


**It is preferred that you do not call getList without parameters as it will
pull down all legislators, if you need to do this feel free to grab the provided
dump of the API data available at http://services.sunlightlabs.com/api/**


search
------

legislators.search allows you to query the database with a less than perfect
representation of a legislator's name.

The search is tolerant of use of nicknames, lastname-firstname juxtaposition,
initials and minor misspellings.  The return is a set of results that include
legislator records as well as certainity scores between 0 and 1 (where 1 is
most certain).

An example usage of search is as follows:

    >>> for r in sunlight.legislators.search('Diane Finestine'):
    ...     print r
    0.92125 Sen. Dianne Feinstein (D-CA)

    
It is also possible to get multiple results:
    
    >>> for r in sunlight.legislators.search('Kennedy'):
    ...     print r
    1.0 Sen. Ted Kennedy (D-MA)
    1.0 Rep. Patrick Kennedy (D-RI)


allForZip
---------

legislators.allForZip retrieves all legislators that represent a given zipcode.

This typically means two senators and one (or more) representatives.

To get all legislators that represent the 27511 zipcode:
    
    >>> for legislator in sunlight.legislators.allForZip(27511):
    ...     print legislator
    Rep. David Price (D-NC)
    Sen. Kay Hagan (D-NC)
    Sen. Richard Burr (R-NC)
    Rep. Brad Miller (D-NC)


-----------------
districts methods
-----------------

The districts namespace is comprised of several functions:
    * districts.getDistrictsFromZip
    * districts.getZipsFromDistrict
    * districts.getDistrictFromLatLong
    

getDistrictsFromZip
-------------------

districts.getDistrictsFromZip fetches all districts that overlap a given
zipcode.

To get all districts that overlap 14623:
    >>> for district in sunlight.districts.getDistrictsFromZip(14623):
    ...     print district
    NY-29
    NY-28


getZipsFromDistrict
-------------------

districts.getZipsFromDistrict fetches all zips that fall within a district.

To get all zipcodes in the NY-29th:
    >>> sunlight.districts.getZipsFromDistrict('NY', 29)
    [u'14925', u'14905', u'14904', u'14903', u'14902', u'14901', u'14898', u'14897', u'14895', u'14894', u'14893', u'14892', u'14891', u'14889', u'14887', u'14886', u'14885', u'14884', u'14883', u'14880', u'14879', u'14878', u'14877', u'14876', u'14874', u'14873', u'14872', u'14871', u'14870', u'14869', u'14867', u'14865', u'14864', u'14863', u'14861', u'14859', u'14858', u'14857', u'14856', u'14855', u'14846', u'14845', u'14843', u'14842', u'14841', u'14840', u'14839', u'14838', u'14837', u'14836', u'14831', u'14830', u'14827', u'14826', u'14825', u'14824', u'14823', u'14822', u'14821', u'14820', u'14819', u'14818', u'14816', u'14815', u'14814', u'14813', u'14812', u'14810', u'14809', u'14808', u'14807', u'14806', u'14805', u'14804', u'14803', u'14802', u'14801', u'14788', u'14786', u'14783', u'14779', u'14778', u'14777', u'14774', u'14772', u'14770', u'14766', u'14760', u'14755', u'14754', u'14753', u'14751', u'14748', u'14747', u'14745', u'14744', u'14743', u'14741', u'14739', u'14738', u'14737', u'14735', u'14731', u'14730', u'14729', u'14727', u'14726', u'14721', u'14719', u'14717', u'14715', u'14714', u'14711', u'14709', u'14708', u'14707', u'14706', u'14625', u'14624', u'14623', u'14620', u'14618', u'14610', u'14606', u'14586', u'14585', u'14572', u'14564', u'14561', u'14560', u'14559', u'14548', u'14547', u'14546', u'14544', u'14543', u'14536', u'14534', u'14532', u'14529', u'14527', u'14526', u'14522', u'14518', u'14514', u'14513', u'14512', u'14507', u'14506', u'14504', u'14502', u'14489', u'14487', u'14485', u'14478', u'14475', u'14472', u'14471', u'14469', u'14467', u'14466', u'14463', u'14461', u'14456', u'14453', u'14450', u'14445', u'14443', u'14441', u'14437', u'14432', u'14428', u'14425', u'14424', u'14418', u'14415', u'14414', u'14173', u'14171', u'14168', u'14141', u'14138', u'14133', u'14129', u'14101', u'14081', u'14070', u'14065', u'14060', u'14042', u'14041', u'14030', u'14029', u'14024', u'14009']

getDistrictFromLatLong
----------------------

districts.getDistrictFromLatLong finds the district that a given lat-long
coordinate pair falls within.

To find out what district 61.13 N, 149.54 W falls within:
    >>> print sunlight.districts.getDistrictFromLatLong(61.13, 149.54)
    AK-0

This point is in fact in Anchorage, Alaska, so this is correct.


-----------------
committee methods
-----------------

The committee namespace contains:
    * committee.getList
    * committee.get
    * committee.allForMember

getList
-------

committee.getList gets all committees for a given chamber (House, Senate, or Joint).

To see all joint committees for the current congress:
    >>> for c in sunlight.committees.getList('Joint'):
    ...     print c
    Joint Economic Committee
    Joint Committee on Printing
    Joint Committee on Taxation
    Joint Committee on the Library

get
---

committee.get gets full details for a given committee, including membership and subcommittees.

Example of getting details for a committee:

    >>> com = sunlight.committees.get('HSAG')
    >>> print com.name
    House Committee on Agriculture
    >>> for sc in com.subcommittees:
    ...     print sc
    Subcommittee on  Conservation, Credit, Energy, and Research
    Subcommittee on Department Operations, Oversight, Nutrition and Forestry
    Subcommittee on General Farm Commodities and Risk Management
    Subcommittee on Horticulture and Organic Agriculture
    Subcommittee on Livestock, Dairy, and Poultry 
    Subcommittee on Rural Development, Biotechnology, Specialty Crops, and Foreign Agriculture
    >>> for m in com.members:
    ...     print m
    Rep. Joe Baca (D-CA)
    Rep. John Boccieri (D-OH)
    Rep. Leonard Boswell (D-IA)
    Rep. Bobby Bright (D-AL)
    Rep. Dennis Cardoza (D-CA)
    Rep. Bill Cassidy (R-LA)
    Rep. Travis Childers (D-MS)
    Rep. Mike Conaway (R-TX)
    Rep. Jim Costa (D-CA)
    Rep. Henry Cuellar (D-TX)
    Rep. Kathy Dahlkemper (D-PA)
    Rep. Brad Ellsworth (D-IN)
    Rep. Jeff Fortenberry (R-NE)
    Rep. Bob Goodlatte (R-VA)
    Rep. Sam Graves (R-MO)
    Rep. Debbie Halvorson (D-IL)
    Rep. Stephanie Herseth Sandlin (D-SD)
    Rep. Tim Holden (D-PA)
    Rep. Tim Johnson (R-IL)
    Rep. Steven Kagen (D-WI)
    Rep. Steve King (R-IA)
    Rep. Larry Kissell (D-NC)
    Rep. Frank Kratovil (D-MD)
    Rep. Bob Latta (R-OH)
    Rep. Frank Lucas (R-OK)
    Rep. Blaine Luetkemeyer (R-MO)
    Rep. Cynthia Lummis (R-WY)
    Rep. Betsy Markey (D-CO)
    Rep. Jim Marshall (D-GA)
    Rep. Eric Massa (D-NY)
    Rep. Mike McIntyre (D-NC)
    Rep. Walt Minnick (D-ID)
    Rep. Jerry Moran (R-KS)
    Rep. Randy Neugebauer (R-TX)
    Rep. Collin Peterson (D-MN)
    Rep. Earl Pomeroy (D-ND)
    Rep. Phil Roe (R-TN)
    Rep. Mike Rogers (R-AL)
    Rep. Mark Schauer (D-MI)
    Rep. Jean Schmidt (R-OH)
    Rep. Kurt Schrader (D-OR)
    Rep. David Scott (D-GA)
    Rep. Adrian Smith (R-NE)
    Rep. G.T. Thompson (R-PA)
    Rep. Tim Walz (D-MN)

allForLegislator
----------------

All for legislator shows all of a legislator's committee and subcommittee memberships.

*note that the subcommittees included are only the subcommittees that the member has a seat on*

Showing all of a legislators committees and subcommittees:
    >>> for com in sunlight.committees.allForLegislator('S000148'):
    ...    print com
    ...    for sc in com.subcommittees:
    ...        print '  ',sc
    Senate Committee on Rules and Administration
    Senate Committee on Finance
       Subcommittee on International Trade and Global Competitiveness
       Subcommittee on Social Security, Pensions and Family Policy
       Subcommittee on Taxation, IRS Oversight, and Long-term Growth
    Joint Committee on the Library
    Joint Economic Committee
    Senate Commmittee on the Judiciary
       Subcommittee on Administrative Oversight and the Courts
       Subcommittee on Antitrust, Competition Policy and Consumer Rights
       Subcommittee on Crime and Drugs
       Subcommittee on Immigration, Refugees and Border Security
       Subcommittee on Terrorism and Homeland Security
    Joint Committee on Printing
    Senate Committee on Banking, Housing, and Urban Affairs
       Subcommittee on Securities, Insurance, and Investment
       Subcommittee on Financial Institutions
       Subcommittee on Housing, Transportation, and Community Development

-----------------
lobbyists methods
-----------------

The lobbyists namespace contains:
    * lobbyists.getFiling
    * lobbyists.getFilingList
    * lobbyists.search
    

getFiling
---------

To get all details on a single filing by id:

    >>> filing = sunlight.lobbyists.getFiling('29D4D19E-CB7D-46D2-99F0-27FF15901A4C')

    >>> print filing
    29D4D19E-CB7D-46D2-99F0-27FF15901A4C - Sunlight Foundation for SUNLIGHT FOUNDATION
    
    >>> for lobbyist in filing.lobbyists:
    ...     print lobbyist
    MICHAEL KLEIN
    ZEPHYR TEACHOUT
    ELLEN MILLER
    NISHA THOMPSON
    
    >>> for issue in filing.issues:
    ...     print issue
    GOVERNMENT ISSUES (unspecified)


getFilingList
-------------

To get all filings of a particular client or registrant:

    >>> for filing in sunlight.lobbyists.getFilingList(client_name='SUNLIGHT FOUNDATION'):
    ...     print filing
    79DAF5B3-3444-4966-A5F1-844A647EB200 - Bernstein Strategy Group for SUNLIGHT FOUNDATION
    04693B31-E97E-4A42-A157-12B4639A4319 - Sunlight Foundation for SUNLIGHT FOUNDATION
    29D4D19E-CB7D-46D2-99F0-27FF15901A4C - Sunlight Foundation for SUNLIGHT FOUNDATION
    03404F3C-3084-4B2E-949F-0788E86E547F - Bernstein Strategy Group for SUNLIGHT FOUNDATION
    713046BC-0EA7-4547-843F-FFD4716BD0EB - Bernstein Strategy Group for SUNLIGHT FOUNDATION
    17E43624-A38F-4E42-9CA3-0BC8737A169A - Sunlight Foundation for SUNLIGHT FOUNDATION
    9BB3FF43-34FF-454C-B796-45DB5CA10EFC - Bernstein Strategy Group for SUNLIGHT FOUNDATION
    4209EEC2-E946-45B7-8B9C-87DF85BD15C2 - Sunlight Foundation for SUNLIGHT FOUNDATION
    C4438A23-7036-4FF0-860B-5EB2FE842AA7 - Bernstein Strategy Group for SUNLIGHT FOUNDATION
    1BB3B0FA-220C-464E-A7D1-F609010ABC0C - Sunlight Foundation for SUNLIGHT FOUNDATION

search
------

To use a fuzzy name-matching search to find lobbyists filings:

    >>> for r in sunlight.lobbyists.search('Nosha Thrompson', year=2008):
    ...     print r
    0.945396825397 NISHA THOMPSON (Sunlight Foundation)


----------------
wordlist methods
----------------

The wordlist namespace is used for maintaining and using lists of words primarily to be used for stopword filtering.

It contains the methods:
* get
* update
* filter_stopwords

get
---

wordlist.get(list_name) gets a stopword list by name.

To get a python list of stopwords:

    >>> sunlight.wordlist.get('test_articles')
    ['a', 'an', 'the']


update
------

wordlist.update(list_name, words) creates or updates a stopword list.

An example would look something like:

    >>> try:
    ...     sunlight.wordlist.update('test_articles', ['a', 'an', 'the'])
    ... except SunlightApiError, e:
    ...     print e
    Attempt to modify wordlist that belongs to another user

**Note that you can only update a wordlist that you created, attempting to
modify someone elses wordlist will result in a 403 - Access Denied error**


filter_stopwords
----------------

Once a wordlist exists the primary use is to remove all stopwords from a block of text using the filter_stopwords method.

An example of using ``filter_stopwords`` for just that:

    >>> sunlight.wordlist.filter_stopwords('test_articles', 'The boy named Frank ate a banana and an apple')
    'boy named frank ate banana and apple'

You'll notice that punctuation has been stripped and capitalized words are no longer capitalized.  This is a side effect of the filtering process that comes in handy when creating word frequency visualizations (the intended purpose of the stopword API)

