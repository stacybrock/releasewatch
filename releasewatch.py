import json
import os
import requests
from github import Github, Auth, UnknownObjectException

import pprint
pp_ = pprint.PrettyPrinter(indent=2)
pp = pp_.pprint

SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))

CONFIG = {}
CONFIG['TARGET_REPOS'] = os.getenv('RELEASEWATCH_TARGET_REPOS', None).split(',')
CONFIG['GITHUB_TOKEN'] = os.getenv('RELEASEWATCH_GITHUB_TOKEN', None)
CONFIG['PUSHOVER_APP_KEY'] = os.getenv('RELEASEWATCH_PUSHOVER_APP_KEY', None)
CONFIG['PUSHOVER_DEVICE'] = os.getenv('PUSHOVER_DEVICE', None)
CONFIG['PUSHOVER_USER_KEY'] = os.getenv('PUSHOVER_USER_KEY', None)

def main():
    auth = Auth.Token(CONFIG['GITHUB_TOKEN'])
    gh = Github(auth=auth)

    # read last notified values from file
    try:
        with open(SCRIPTPATH + '/last_notified.cache', 'r') as CACHEFILE:
            raw = CACHEFILE.read()
    except FileNotFoundError:
        raw = ''

    if raw == '':
        notified_releases = {}
    else:
        notified_releases = json.loads(raw)

    for repo_name in CONFIG['TARGET_REPOS']:
        repo = gh.get_repo(repo_name)

        # get most recent release on repo
        try:
            last_release = repo.get_latest_release()
        except UnknownObjectException:
            # repo has no releases
            continue

        # check if release has changed since the last notified release
        if last_release.name != notified_releases.get(repo.full_name):
            # create pushover notification
            title = f"{repo.full_name} released {last_release.name}"
            msg = (f"{repo.full_name} has released '{last_release.name}': "
                   f"{last_release.html_url}")
            r = requests.post('https://api.pushover.net/1/messages.json', data={
                'token': CONFIG['PUSHOVER_APP_KEY'],
                'user': CONFIG['PUSHOVER_USER_KEY'],
                'message': msg,
                'title': title,
                'device': CONFIG['PUSHOVER_DEVICE']
            })

            notified_releases[repo.full_name] = last_release.name

    # write last notified values to file
    with open(SCRIPTPATH + '/last_notified.cache', 'w') as CACHEFILE:
        CACHEFILE.write(json.dumps(notified_releases))

if __name__ == '__main__':
    main()
