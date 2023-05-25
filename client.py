import json
import os
import subprocess
import sys

settings = {
    'inspection': {
        'update': True,
        'requirement': True
    }
}

if __name__ == '__main__':
    if os.path.exists('.settings.json'):
        with open('.settings.json', 'r') as config:
            settings.update(json.load(config))

    python = sys.executable
    if settings['inspection']['requirement']:
        subprocess.check_call([python, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        settings['inspection']['requirement'] = False

    import git

    if settings['inspection']['update']:
        with git.Repo('.') as repo:
            try:
                remote = repo.remote()
            except ValueError:
                remote = repo.create_remote('origin', 'https://gitee.com/Legoshi/smartpond-client.git')
            infos = remote.fetch()
            print(infos)
            settings['inspection']['requirement'] = True
    with open('.settings.json', 'w') as file:
        json.dump(settings, file)

    import client.main as client

    client.main()
