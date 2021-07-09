#!/usr/bin/python3
import os,logging
import jeopardy_sync.reddit as reddit
from jeopardy_sync.gdrive import GDriveClient
from jeopardy_sync.config import JSyncConfig
from pathlib import Path


DEFAULT_ROOT = os.path.join(str(Path.home()),"jsync")

SUPPORTED_VIDEO_EXTENSIONS = {
    '.mp4',
    '.mkv',
    '.wbem'
}

class JSync(object):
    def __init__(self):
        self.config = JSyncConfig(os.path.join(DEFAULT_ROOT,"jsync.conf"))
        self.gdrive = None
        self.is_valid = self.init_sync()

    def init_sync(self):
        # Create output directory if it doesn't exist.
        if(not os.path.exists(self.config.output_path)):
            os.makedirs(self.config.output_path)
        # Initialize GDrive Object
        self.gdrive = GDriveClient(root_path=os.path.join(DEFAULT_ROOT,'gdrive'))
        if(self.gdrive.is_valid is False):
            return False



    def get_episode_file_ids(self,reddit_user_list):
        result_list = []
        try:
            for entry in reddit_user_list:
                result_list.extend(reddit.search_gdrive_ids_by_user(entry))
        except Exception as e:
            print("Error Getting Episode FileIDs from Reddit")
            print(e)
            return False,result_list

        return True,result_list

    def sync(self):
        # Get File IDs
        files_to_download = {}
        logging.debug("Get File IDs...")
        result,fids = self.get_episode_file_ids(self.config.reddit_user_list)
        if(result is False):
            logging.error("Error Scraping Reddit :(")
            return False

        # Get Metadata for each FID
        for entry in fids:
            try:
                entry_metadata = self.gdrive.stat(entry)
            except: # Skip Dead Files
                logging.warning("Dead File: %s" % entry)
                continue
            # Skip stuff that is not video
            entry_ext = os.path.splitext(entry_metadata['name'])[-1].lower()
            if(not entry_ext in SUPPORTED_VIDEO_EXTENSIONS):
                continue
            # Skip stuff we have already downloaded
            if(entry_metadata['md5Checksum'] in self.config.hash_db.keys()):
                continue
            # Download File
            logging.info("Downloading %s..." % entry_metadata['name'])
            file_output_path = os.path.join(self.config.output_path, entry_metadata['name'])

            try:
                self.gdrive.download(entry,file_output_path)
            except Exception as e:
                logging.error("Exception while downloading")
                logging.error(e)

            # If Successful, update hash db.
            if(os.path.exists(file_output_path) and os.path.getsize(file_output_path) == entry_metadata['size']):
                logging.info("Downloaded %s..." % entry_metadata['name'])
                self.config.update_hashdb(entry_metadata['md5Checksum'])
            else:
                logging.warning("Error Downloading: %s" % entry_metadata['name'])
        return True