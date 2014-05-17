#!/usr/bin/python
# coding=utf-8
import os.path
import sys
import urllib2 as urllib
import json

__author__ = 'Victor Häggqvist'
__version__ = '0.1.1'

def searchGithub(query):
  url = "https://api.github.com/search/code?q="+query+"+repo:github/gitignore"
  accept = "application/vnd.github.v3+json"
  userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.8 Safari/537.36"

  request = urllib.Request(url, headers={"Accept": accept, "User-Agent": userAgent})

  content = ""
  try:
    content = urllib.urlopen(request).read()
  except urllib.HTTPError as e:
    print "Some thing faild... HTTP error:",e.code

  response = json.loas(content)
  if response["total_count"] == 0:
    print query,"not found"
  else:
    print "Got",response["total_count"],"hits"
    for item in response["items"]:
      print item["name"]

def gitiglobal(type):
  """
  Fetch gitignore from the global directory
  """
  print "Fetching .gitignore for", type,"in Global"
  try:
    gifile =  urllib.urlopen("https://raw.githubusercontent.com/github/gitignore/master/Global/"+type+".gitignore").read()
    store(gifile)
  except urllib.HTTPError as e:
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
    gifile = urllib.urlopen("https://raw.githubusercontent.com/github/gitignore/master/"+type+".gitignore").read()
    store(gifile)
  except urllib.HTTPError as e:
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

if __name__ == "__main__":
  main()
