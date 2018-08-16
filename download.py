#!/usr/bin/env python
"""
Redownload asset files.

"""

import os
import shutil
import subprocess
import sys
import ast
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


VENDOR_ASSETS = {
    "jquery-1.11.0.min.js": "https://code.jquery.com/jquery-1.11.0.min.js",
    "jquery.flot-0.8.2.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.min.js",
    "jquery.flot-0.8.2.time.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.time.min.js",
    "jquery.flot-0.8.2.selection.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.selection.min.js",
    "jquery.flot-0.8.2.categories.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.categories.min.js",
    "bootstrap-3.1.0.min.js": "https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js",
    "bootstrap-3.1.0.min.css": "https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css"
}

VENDOR_DIR = os.path.abspath(os.path.dirname(__file__))


def download_assets():
    if not os.path.isdir(VENDOR_DIR):
        os.makedirs(VENDOR_DIR)

    for fn, asset in sorted(VENDOR_ASSETS.items()):
        dst = os.path.join(VENDOR_DIR, fn)

        if os.path.isfile(dst):
            continue

        print("Downloading {0} to asv/www/vendor...".format(asset))

        fsrc = urlopen(asset)
        try:
            with open(dst + ".new", 'wb') as fdst:
                shutil.copyfileobj(fsrc, fdst)
        finally:
            fsrc.close()

        # Usually atomic
        os.rename(dst + ".new", dst)


if __name__ == "__main__":
    download_assets()
