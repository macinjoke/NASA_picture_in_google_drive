import requests
import httplib2
import os
import shutil
from google_drive_credential import get_credentials
from apiclient import discovery
from googleapiclient.http import MediaFileUpload

from api_keys import NASA_API_KEY


FOLDER_ID = '0B7BAGrsUmzTea0FqcWZ0eEYxdXM'
MIME_TYPE = 'image/jpeg'
SAVED_FILE = os.path.expanduser('~/.ghq/github.com/tonkatu05/NASA_picture_in_google_drive/astronomy.jpg')
NASA_API_URL = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(NASA_API_KEY)


def fetch_nasa_image(url):
    r = requests.get(url)
    body = r.json()
    image_url = body['hdurl']
    return image_url


def upload_file(file_name):
    print('upload "{}" to google drive'.format(file_name))
    media_body = MediaFileUpload(file_name, mimetype=MIME_TYPE, resumable=True)
    body = {
        'name': os.path.split(file_name)[-1],
        'mimeType': MIME_TYPE,
        'parents': [FOLDER_ID],
    }
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
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

if __name__ == '__main__':
    image_url = fetch_nasa_image(NASA_API_URL)
    save_from_remote_to_local(image_url, SAVED_FILE)
    upload_file(SAVED_FILE)
