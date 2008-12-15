from distutils.core import setup
from sunlightapi import __version__,__license__,__doc__

license_text = open('LICENSE').read()
long_description = open('README.rst').read()

setup(name="python-sunlightapi",
      version=__version__,
      py_modules=["sunlightapi"],
      description="Libraries for interacting with the Sunlight Labs API",
      author="James Turk",
      author_email = "jturk@sunlightfoundation.com",
      license=license_text,
      url="http://github.com/sunlightlabs/python-sunlightapi/",
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

