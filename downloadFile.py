import os
import requests


def downloadFile(url, download_directory, filename=''):
    try:
        if filename:
            pass
        else:
            filename = url[url.rfind('/')+1:]

        with requests.get(url) as req:
            with open(os.path.join(download_directory, filename), 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename

    except Exception as e:
        return e
