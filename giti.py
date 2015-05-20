#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import requests

__author__ = 'Victor Häggqvist'
__version__ = '0.2'


def repo_url(kind: str, global_dir=False) -> str:
    if global_dir:
        return 'https://raw.githubusercontent.com/github/gitignore/master/Global/%s.gitignore' % kind
    else:
        return 'https://raw.githubusercontent.com/github/gitignore/master/%s.gitignore' % kind


def get_ignore_file(kind: str, global_dir=False, path=False) -> str:
    """
    Download the file
    """
    if not path:
        url = repo_url(kind, global_dir)
    else:
        if kind[0] == '/':
            kind = kind[1:]
        url = 'https://raw.githubusercontent.com/github/gitignore/master/%s' % kind

    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.text


def search_for_file(kind: str) -> str:
    """
    Search for file in https://github.com/github/gitignore
    """
    headers = {
        'User-Agent': 'giti.py/0.0.1',
        'Accept': 'application/vnd.github.v3+json'
    }
    r = requests.get('https://api.github.com/search/code?q=repo:github/gitignore %s' % kind, headers=headers)
    cont = r.json()

    print('One of these might be good:')
    for i in range(0, len(cont['items'])):
        name = cont['items'][i]['name'].split('.')[0]
        print('[%s] %s' % (i, name))

    try:
        choice = int(input('Enter index: '))
    except TypeError:
        return None
    except KeyboardInterrupt:
        return None

    if -1 < choice < len(cont['items']):
        return cont['items'][choice]['path']
    else:
        return None


def save_file(file: str):
    """
    Store content in file
    """
    merge = 'y'
    replace = 'n'
    if os.path.isfile('.gitignore'):
        try:
            merge = input('Do you want to merge with existing .gitignore [Y/n]: ')
            merge = 'y' if merge == '' else 'n'
        except KeyError:
            merge = 'y'

        if merge.lower() == "n":
            try:
                replace = input('Do you want to replace existing .gitignore [y/N]: ')
            except KeyError:
                replace = 'n'

    if merge.lower() == 'y':
        with open('.gitignore', 'a') as f:
            f.write(file)
        print('.gitignore baked :)')

    elif replace.lower() == 'y':
        with open('.gitignore', 'w') as f:
            f.write(file)
        print('.gitignore replaced')

    else:
        print('Did nothing, your .gitignore lives like before')


def giti(kind: str):
    kind = kind[0].upper() + kind[1:]
    print('Fetching .gitignore for %s' % kind)

    gifile = get_ignore_file(kind)

    if not gifile:
        print('Not found in master')
        gifile = get_ignore_file(kind, global_dir=True)

    if not gifile:
        print('Found no exact match, let\'s give searching a try...')
        filepath = search_for_file(kind)
        if not filepath:
            print('Can\'t help any more, exiting')
            print('No changes made')
            exit(0)
        gifile = get_ignore_file(filepath, path=True)

    if not gifile:
        print('Can\'t help any more, exiting')
        print('No changes made')
        exit(0)

    save_file(gifile)


def show_help():
    print('Usage: giti [language or stuff]')
    print('giti v%s' % __version__)


def main():
    if len(sys.argv) == 2:
        giti(sys.argv[1])
    else:
        show_help()

if __name__ == '__main__':
    main()
