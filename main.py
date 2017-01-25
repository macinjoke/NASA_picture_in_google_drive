import requests
import httplib2
import os
import shutil
from google_drive_credential import get_credentials
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload

from api_keys import NASA_API_KEY


FOLDER_ID = '0B7BAGrsUmzTea0FqcWZ0eEYxdXM'
MIME_TYPE = 'image/jpeg'
SAVED_FILE = os.path.expanduser('~/.ghq/github.com/tonkatu05/NASA_picture_in_google_drive/astronomy.jpg')
NASA_API_URL = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(NASA_API_KEY)

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)


def upload_file(file, file_name):
    print('upload "{}" to google drive'.format(file))
    media_body = MediaFileUpload(file, mimetype=MIME_TYPE, resumable=True)
    body = {
        'name': file_name,
        'mimeType': MIME_TYPE,
        'parents': [FOLDER_ID],
    }
    service.files().create(body=body, media_body=media_body).execute()
    print('uploaded')


def save_from_remote_to_local(url, saved_file):
    print('save from {} to {}'.format(url, saved_file))
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(saved_file, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            print('saved')
    else:
        print(r.status_code)


def copy_picture_for_wallpaper():
    results = service.files().list(q="'0B7BAGrsUmzTea0FqcWZ0eEYxdXM' in parents and trashed = false",
                                   orderBy='createdTime desc').execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('{} files were founded:'.format(len(items)))
        for i, item in enumerate(items):
            # ５つまでしか貯めない
            if i == 5:
                break
            print('name: {}, id: {}'.format(item['name'], item['id']))
            new_file_body = {
                'name': '{0:02d}_{1}.jpg'.format((len(items) if len(items) < 5 else 5) - i, item['name']),
                'parents': ['0B7BAGrsUmzTeOGE4ekc5a29yMlU'],
            }
            print('copy {}'.format(item['name']))
            service.files().copy(fileId=item['id'], body=new_file_body).execute()
            print('copied')


if __name__ == '__main__':
    r = requests.get(NASA_API_URL)
    body = r.json()
    image_url = body['hdurl']
    save_from_remote_to_local(image_url, SAVED_FILE)
    upload_file(SAVED_FILE, '{}.jpg'.format(body['date']))
    copy_picture_for_wallpaper()
