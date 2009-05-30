from distutils.core import setup
from ideascaleapi import __version__,__license__,__doc__

license_text = open('LICENSE').read()
long_description = open('README.rst').read()

setup(name="python-ideascaleapi",
      version=__version__,
      py_modules=["ideascaleapi"],
      description="Libraries for interacting with the Ideascale API",
      author="Greg Elin (forking James Turk)",
      author_email = "greg@fotonotes.net",
      license=license_text,
      url="http://github.com/gregelin/python-ideascaleapi/tree/master",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
       install_requires=["simplejson >= 1.8"]
      )

