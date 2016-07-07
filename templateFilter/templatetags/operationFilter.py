#coding=utf8
from django import template
register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):  
    return value * arg

@register.filter(name='catNLPID')
def catNLPID(nlpList):
    print 233
    print nlpList
    return ",".join([str(nlpID) for nlpID, nlpName in nlpList])

@register.filter(name='catNLPName')
def catNLPName(nlpList):
    return ";<br>".join([nlpName for nlpID, nlpName in nlpList])