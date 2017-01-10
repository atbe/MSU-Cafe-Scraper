from pathlib import Path
from time import time

from CafeScraper.Scraper import Scraper
import json

def collect_backup_and_dump():

    '''
    Get the new json
    '''
    scraper = Scraper()
    json_dump = json.dumps(list(scraper.cafes_dict.values()), default=lambda c: c.__dict__, sort_keys=True)

    '''
    Backup this json
    '''
    # check if backup folder exists
    BACKUP_PATH_NAME = "backup_menu_json"
    cwd = Path('.')
    if not (cwd / BACKUP_PATH_NAME).exists():
        # create it if it doesn't
        print("DEBUG: backup folder did not exist, creating now...")
        (cwd / BACKUP_PATH_NAME).mkdir(mode=0o744)

    # epoch time this new json was created in seconds rounded to the nearest integer
    new_backup_file_name = str(int(time())) + '_menus_save.json'
    absolute_path = str((cwd / BACKUP_PATH_NAME).absolute()) + '/' + new_backup_file_name
    with open(absolute_path, 'w') as fp:
        print(json_dump, file=fp)

    '''
    Distribute the new json
    '''
    with open('menus.json', 'w') as fp:
        print(json_dump, file=fp)

if __name__ == '__main__':
    collect_backup_and_dump()
