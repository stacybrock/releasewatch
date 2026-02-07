import os
import requests
from github import Github, Auth

import pprint
pp_ = pprint.PrettyPrinter(indent=2)
pp = pp_.pprint

SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))

CONFIG = {}
CONFIG['TARGET_REPO'] = os.getenv('RELEASEWATCH_TARGET_REPO', None)
CONFIG['GITHUB_TOKEN'] = os.getenv('RELEASEWATCH_GITHUB_TOKEN', None)
CONFIG['PUSHOVER_APP_KEY'] = os.getenv('RELEASEWATCH_PUSHOVER_APP_KEY', None)
CONFIG['PUSHOVER_DEVICE'] = os.getenv('PUSHOVER_DEVICE', None)
CONFIG['PUSHOVER_USER_KEY'] = os.getenv('PUSHOVER_USER_KEY', None)

def main():
    auth = Auth.Token(CONFIG['GITHUB_TOKEN'])
    gh = Github(auth=auth)
    repo = gh.get_repo(CONFIG['TARGET_REPO'])

    # read last notified patch value from file
    try:
        with open(SCRIPTPATH + '/last_notified.cache', 'r') as CACHEFILE:
            raw = CACHEFILE.read()
    except FileNotFoundError:
        raw = ''

    if raw == '':
        notified_release = ''
    else:
        notified_release = raw.strip()

    # get most recent release on repo
    last_release = repo.get_latest_release()

    # check if release has changed since the last notified release
    if last_release.name != notified_release:
        # create pushover notification
        title = f"{repo.full_name} released {last_release.name}"
        msg = (f"{repo.full_name} has released '{last_release.name}': "
               f"{last_release.html_url}")
        r = requests.post('https://api.pushover.net/1/messages.json', data = {
            'token': CONFIG['PUSHOVER_APP_KEY'],
            'user': CONFIG['PUSHOVER_USER_KEY'],
            'message': msg,
            'title': title,
            'device': CONFIG['PUSHOVER_DEVICE']
        })

        with open(SCRIPTPATH + '/last_notified.cache', 'w') as CACHEFILE:
            CACHEFILE.write(last_release.name)

if __name__ == '__main__':
    main()
