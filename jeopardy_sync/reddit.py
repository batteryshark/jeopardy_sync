#!/usr/bin/python3
import re
import requests
USERNAME_BASE_URL = "https://www.reddit.com/user/"


def get_page_content(user_url, current_count=0, after_tag=""):
    headers = {'user-agent': 'Mozilla/5.0'}
    params = {}
    if (current_count > 0 and after_tag != ""):
        params['count'] = current_count
        params['after'] = after_tag
    r = requests.get(user_url, params=params, headers=headers)
    if (r.status_code != 200):
        return None
    else:
        return r.content


def search_gdrive_ids_by_user(username):
    current_count = 0
    fid_db = {}
    after_tag = ""
    while 1:
        last_count = current_count
        content = get_page_content(USERNAME_BASE_URL+username, current_count, after_tag)
        if (content == None):
            break
        else:

            content = content.decode('ascii',errors='replace')
            urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", content)
            for ur in urls:
                cfid = carve_gdrive_fid(ur)
                if (cfid != ""):
                    fid_db[cfid] = ""

                current_count, after_tag = carve_next_page(ur,current_count,after_tag)
            if (last_count == current_count):
                break

    return fid_db.keys()

def carve_next_page(url,current_count,after_tag):
    if (USERNAME_BASE_URL in url and 'after=' in url):
        count_start = url.find("count=") + len("count=")
        count_end = url[count_start:].find("&") + count_start
        current_count = url[count_start:count_end]
        tag_start = url.find("after=") + len("after=")
        after_tag = url[tag_start:]

    return current_count, after_tag


def carve_gdrive_fid(url):
    # Hack to peel off the file id
    if ("drive.google.com" in url):
        if ("open?id=" in url):
            start_offset = url.find("open?id=") + len("open?id=")
            return url[start_offset:start_offset+33]

    return ''




