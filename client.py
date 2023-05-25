if __name__ == '__main__':
    settings = {
        'inspection': {
            'update': True,
            'requirement': True
        }
    }

    import os

    if os.path.exists('.settings.json'):
        import json

        with open('.settings.json', 'r') as config:
            settings.update(json.load(config))

    import sys
    import subprocess

    python = sys.executable
    if settings['inspection']['requirement']:
        subprocess.check_call([python, '-m', 'pip', 'install', '-r', 'requirements.txt'])

    import git

    if settings['inspection']['update']:
        with git.Repo('.') as repo:
            try:
                remote = repo.remote()
            except ValueError:
                remote = repo.create_remote('origin', 'https://gitee.com/Legoshi/smartpond-client.git')
            remote.fetch()

    import client.main as client

    client.main()
