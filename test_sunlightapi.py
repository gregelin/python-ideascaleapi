import doctest

print 'Before testing be sure to set your key in sunlightapi.txt..\n\n'

doctest.testfile('sunlightapi.rst', verbose=True)
