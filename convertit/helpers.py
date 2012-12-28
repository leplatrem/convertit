import os
from urlparse import urlsplit
from datetime import datetime


def remove_files_older_than(limit, path):
    for basename in os.listdir(path):
        target = os.path.join(path, basename)
        target_mtime = os.path.getmtime(target)
        target_datetime = datetime.fromtimestamp(target_mtime)
        now_datetime = datetime.now()
        time_delta = now_datetime - target_datetime
        if time_delta.seconds > limit:
            os.remove(target)


def render_converted_name(template, url, extension):
    parsed_url = urlsplit(url)
    url_dirname = os.path.dirname(parsed_url.path)[1:].replace('/', '_')
    url_basename = os.path.basename(parsed_url.path)
    url_filename, url_extension = os.path.splitext(url_basename)

    data = {
        'url_hostname': parsed_url.hostname,
        'url_port': parsed_url.port,
        'url_dirname': url_dirname,
        'url_filename': url_filename,
        'url_extension': url_extension or '',
        'extension': extension,
    }

    return template.format(**data)
