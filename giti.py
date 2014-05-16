#!/usr/bin/python
# coding=utf-8
import os
import sys
import urllib2

__author__ = 'Victor Häggqvist'
__version__ = '0.1.1'


def gitiglobal(type):
  """
  Fetch gitignore from the global directory
  """
  print "Fetching .gitignore for", type,"in Global"
  try:
    gifile =  urllib2.urlopen("https://raw.githubusercontent.com/github/gitignore/master/Global/"+type+".gitignore").read()
    store(gifile)
  except urllib2.HTTPError as e:
    if e.code == 404:
      print "Not found in global either"
    else:
      print "Got unexpected answer from Github, you better check on them..."


def store(file):
  """
  Store content in file
  """
  if os.path.isfile(".gitignore") == True:
    try:
      merge = input("Do you want to merge with existing .gitignore [Y/n]:")
    except:
      merge = "y"
    existingFile = open(".gitignore").read()
  else:
    merge = "y"
    existingFile = ""

  if merge.lower() == "y":
    gitignore = existingFile + file
    f = open('.gitignore', 'w')
    f.write(gitignore)
    print ".gitignore baked :)"
  else:
    print "Did nothing, your .gitignore lives like before"


def giti(type):
  """
  Fetch gitignore from directory
  """
  type = type[0].upper() + type[1:] # make first upper
  print "Fetching .gitignore for", type

  try:
    gifile = urllib2.urlopen("https://raw.githubusercontent.com/github/gitignore/master/"+type+".gitignore").read()
    store(gifile)
  except urllib2.HTTPError as e:
    if e.code == 404:
      print "Not found in master"
      gitiglobal(type)
    else:
      print "Got unexpected answer from Github, you better check on them..."


def help():
  print "Usage: giti [language or stuff]"
  print "giti v"+__version__


def main():
  if len(sys.argv) == 2:
    giti(sys.argv[1])
  else:
    help()

main()
