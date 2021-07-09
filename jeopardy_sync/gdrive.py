#!/usr/bin/python3

import os,platform,logging
import httplib2
from pathlib import Path
from apiclient import discovery
import argparse
from oauth2client import client,tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

if(platform.system() == "Windows"):
    DEFAULT_SERVICE_ROOT = os.path.join(str(Path.home()), 'gdrive')
else:
    DEFAULT_SERVICE_ROOT = os.path.join(str(Path.home()), '.gdrive')
DEFAULT_APPLICATION_NAME = 'JKL Redux V3'
DEFAULT_SCOPES = 'https://www.googleapis.com/auth/drive'
DEFAULT_CLIENT_SECRET_FILE = 'credentials.json'
DEFAULT_CHUNKSIZE = (1024 * 1024) * 100


class GDriveClient(object):
    def __init__(self,root_path=DEFAULT_SERVICE_ROOT):
        self.client_secret_path = os.path.join(root_path,DEFAULT_CLIENT_SECRET_FILE)
        self.scopes = DEFAULT_SCOPES
        self.application_name = DEFAULT_APPLICATION_NAME
        self.service_root = DEFAULT_SERVICE_ROOT

        self.is_valid,self.service = self.create()
        self.chunksize = DEFAULT_CHUNKSIZE


    def get_credentials(self,credential_path,refresh=False):
        store = Storage(credential_path)
        credentials = store.get()
        if (credentials == None):
            logging.error("No Credentials")

        if not credentials or credentials.invalid:
            logging.info("Re Authenticate")
            flow = client.flow_from_clientsecrets(self.client_secret_path, self.scopes)
            flow.user_agent = self.application_name
            credentials = tools.run_flow(flow, store, flags)

            logging.debug('Storing credentials to ' + credential_path)
        return True,credentials

    def create(self,nickname="default"):
        try:
            if(not os.path.exists(self.service_root)):
                os.makedirs(self.service_root)
            credential_path = os.path.join(self.service_root, "%s.json" % nickname)
            if(not os.path.exists(credential_path)):
                with open(credential_path, 'a'):
                    os.utime(credential_path, None)
            result,credentials = self.get_credentials(credential_path)
            if(result is False):
                return False,None
            service = discovery.build('drive', 'v3', http=credentials.authorize(httplib2.Http()))
            if(service is None):
                return False,None
            return True,service
        except Exception as e:
            logging.error("GDriveClient Create Error")
            print(e)
            return False,None

        return False,None

    def stat(self, file_id):
        return self.service.files().get(fileId=file_id, fields="md5Checksum,name,size").execute()

    def ls(self,parent_id):
        items = []
        page_token = None
        while True:
            results = self.service.files().list(q="'%s' in parents" % parent_id, spaces='drive',
                                           fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
            items.extend(results.get('files', []))
            page_token = results.get('nextPageToken', None)
            print(page_token)
            if page_token is None:
                break
        return items

    def download(self,file_id,output_path=None):
        if(output_path == None):
            output_path = os.path.join(".",file_id)
        with open(output_path,"wb") as fh:
            downloader = MediaIoBaseDownload(fh, self.service.files().get_media(fileId=file_id), chunksize=self.chunksize)
            done = False
            while done is False:
                status,done = downloader.next_chunk()
                logging.debug("Download %d%%." % int(status.progress() * 100))

    def upload(self,parent_id,input_path):
        file_metadata = {
            'name': os.path.split(input_path)[-1],
            'parents': [parent_id]
        }
        media = MediaFileUpload(input_path, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.debug("File Uploaded")
        return file.get('id')



    def find_file(self, filename):
        page_token = None
        while True:
            response = self.service.files().list(q="""name = "%s" """ % filename,
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                return file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return ""