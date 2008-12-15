from distutils.core import setup
from sunlightapi import __version__,__license__,__doc__

setup(name="python-sunlightapi",
      version=__version__,
      py_modules=["sunlightapi"],
      description="Libraries for interacting with the Sunlight Labs API",
      author="James Turk",
      author_email = "jturk@sunlightfoundation.com",
      license=__license__,
      url="http://github.com/sunlightlabs/python-sunlightapi/",
      long_description=__doc__,
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

