import requests
import httplib2
import os
import shutil
from google_drive_credential import get_credentials
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload

from api_keys import NASA_API_KEY


UPLOAD_FOLDER_ID = '0B7BAGrsUmzTea0FqcWZ0eEYxdXM'
COPIED_FOLDER_ID = '0B7BAGrsUmzTeOGE4ekc5a29yMlU'
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
        'parents': [UPLOAD_FOLDER_ID],
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
    results = service.files().list(q="'{}' in parents and trashed = false".format(UPLOAD_FOLDER_ID),
                                   orderBy='createdTime').execute()
    uploaded_items = results.get('files', [])
    if not uploaded_items:
        print('No files found.')
    else:
        print('{} files were founded:'.format(len(uploaded_items)))
        results = service.files().list(q="'{}' in parents and trashed = false".format(COPIED_FOLDER_ID),
                                       orderBy='createdTime').execute()
        copied_items = results.get('files', [])
        # コピー用フォルダの中の画像ファイルが5つ以下なら、5つになるまでコピーをする。
        if len(copied_items) < 5:
            for item in uploaded_items[-(5 - len(copied_items)):]:
                print('copy `name: {}, id: {}`'.format(item['name'], item['id']))
                new_file_body = {
                    'name': item['name'],
                    'parents': [COPIED_FOLDER_ID],
                }
                service.files().copy(fileId=item['id'], body=new_file_body).execute()
                print('copied')
        # コピー用フォルダの中の画像ファイルが5つなら、一番古い画像を1つ削除し、新しい画像を1つコピーする
        else:
            service.files().delete(fileId=copied_items[0]['id']).execute()
            print('deleted `name: {}, id: {}`'.format(copied_items[0]['name'], copied_items[0]['id']))
            item = uploaded_items[-1:][0]
            print('copy `name: {}, id: {}`'.format(item['name'], item['id']))
            new_file_body = {
                'name': item['name'],
                'parents': [COPIED_FOLDER_ID],
            }
            service.files().copy(fileId=item['id'], body=new_file_body).execute()


if __name__ == '__main__':
    r = requests.get(NASA_API_URL)
    body = r.json()
    image_url = body['hdurl']
    save_from_remote_to_local(image_url, SAVED_FILE)
    upload_file(SAVED_FILE, '{}.jpg'.format(body['date']))
    copy_picture_for_wallpaper()
