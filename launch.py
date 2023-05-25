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


def save_settings():
    with open('.settings.json', 'w') as file:
        json.dump(settings, file)


def main():
    if os.path.exists('.settings.json'):
        with open('.settings.json', 'r') as config:
            settings.update(json.load(config))

    python = sys.executable
    if settings['inspection']['requirement']:
        subprocess.check_call([python, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        settings['inspection']['requirement'] = False
        save_settings()

    import git

    if settings['inspection']['update']:
        with git.Repo('.') as repo:
            try:
                remote = repo.remote()
            except ValueError:
                remote = repo.create_remote('origin', 'https://gitee.com/Legoshi/smartpond-client.git')
            info = remote.pull()[0]
            if info.flags != 4:
                settings['inspection']['requirement'] = True
                save_settings()
                os.execl(python, python, *sys.argv)
                return

    import client.main as client

    client.main()


if __name__ == '__main__':
    main()
