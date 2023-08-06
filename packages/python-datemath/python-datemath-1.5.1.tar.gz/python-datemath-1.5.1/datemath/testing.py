# !/usr/bin/python
# coding=utf-8

from helpers import parse


def dm(expr, **kwargs):
    ''' does our datemath and returns an arrow object '''
    return parse(expr, **kwargs)

def datemath(expr, **kwargs):
    ''' does our datemath and returns a datetime object '''
    return parse(expr, **kwargs).datetime

print(dm(1451610061))

print(dm('1451610061'))

print(datemath(1367900664))
#print(dm(1451610061000))

# print(dm('now-1d/y'))

# try:
#     print(dm('+1ö'))
    
# except Exception as e:
#     print(e)
#    pass


# try: 
#     print(dm('+1.'))
# except Exception as e:
#     print(e)
#     pass