import re
import requests
import zipfile
import io
import shutil
import os

from packaging import version

ADDONS_FOLDER = 'C:\Games\World of Warcraft\_classic_\Interface\AddOns'
ELVUI_FOLDER_NAME = 'ElvUI'
ELVUI_LIBRARIES_FOLDER_NAME = 'ElvUI_Libraries'
ELVUI_OPTIONS_FOLDER_NAME = 'ElvUI_Options'
ELVUI_WRATH_TOC = 'ElvUI_Wrath.toc'
BACKUP_FOLDER = 'BackupElvUI'
BACKUP_BACKUP_FOLDER = 'BackupElvUIBackup'

ELVUI_API_URL = 'https://api.tukui.org/v1/addons'

remote_json = None

def get_local_elvui_version():
    f = open(ADDONS_FOLDER + '\\' + ELVUI_FOLDER_NAME + '\\' + ELVUI_WRATH_TOC,"r")
    lines = f.readlines()
    lines = "".join(lines)
    version = re.search("Version: ([^\n]+)\n", lines).group(1)
    return version

def get_remote_elvui_json():
    global remote_json
    if remote_json is None:
        response = requests.get(ELVUI_API_URL)
        json = response.json()
        for each in json:
            if each['name'] == 'ElvUI':
                remote_json = each
                break
    return remote_json

def get_remote_elvui_version(json):
    return json['version']

def update_needed():
    local_version = get_local_elvui_version()
    remote_json = get_remote_elvui_json()
    remote_version = get_remote_elvui_version(remote_json)
    if version.parse(local_version) < version.parse(remote_version):
        return True
    return False

def download_elvui():
    json = get_remote_elvui_json()
    url = json['url']
    print('Downloading version', json['version'], end='')
    r = requests.get(url, allow_redirects=True)
    print('...done')
    
    print('Extracting ElvUI to', ADDONS_FOLDER, end='')
    with zipfile.ZipFile(io.BytesIO(r.content), 'r') as zip_ref:
        zip_ref.extractall(ADDONS_FOLDER)
    print(' ...done')

def backup_local_elvui():    
    backup_backup_path = ADDONS_FOLDER + '\\' + BACKUP_BACKUP_FOLDER
    backup_path = ADDONS_FOLDER + '\\' + BACKUP_FOLDER
    if(os.path.isdir(backup_backup_path)):
        print('Deleting old backup', end='')
        shutil.rmtree(backup_backup_path)
        print(' ...done')
    if(os.path.isdir(backup_path)):    
        print('Backing up backup', end='')
        shutil.move(backup_path, backup_backup_path)
        print(' ...done')    
    print('Backing up ElvUI', end='')
    shutil.move(ADDONS_FOLDER + '\\' + ELVUI_FOLDER_NAME, ADDONS_FOLDER + '\\' + BACKUP_FOLDER + '\\' + ELVUI_FOLDER_NAME)
    print(' ... done')
    print('Backing up ElvUI Libraries', end='')
    shutil.move(ADDONS_FOLDER + '\\' + ELVUI_LIBRARIES_FOLDER_NAME, ADDONS_FOLDER + '\\' + BACKUP_FOLDER + '\\' + ELVUI_LIBRARIES_FOLDER_NAME)
    print(' ... done')
    print('Backing up ElvUI Options', end='')
    shutil.move(ADDONS_FOLDER + '\\' + ELVUI_OPTIONS_FOLDER_NAME, ADDONS_FOLDER + '\\' + BACKUP_FOLDER + '\\' + ELVUI_OPTIONS_FOLDER_NAME)
    print(' ... done')


def main():
    if update_needed():
        print('Update needed, continuing...')
        backup_local_elvui()
        download_elvui()
    else:
        print('Already up-to-date')
        
    
if __name__ == "__main__":
    main()
