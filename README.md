# JeopardySync Client
### Scrapes reddit for gdrive-uploaded Jeopardy! episodes and downloads them.

### Instructions:
1. Get a GoogleDrive API Key (https://support.google.com/googleapi/answer/6158862?hl=en)

2. Place the "credentials.json" file downloaded from the GDrive API Dashboard into ~/jsync/gdrive/

3. Configure the sync client by editing a copy of the included jsync.conf.sample and placing it at ~/jsync/jsync.conf

4. Run bin/run_jsync.py to scrape and download episodes to the root path specified in the configuration file.


