#!/usr/bin/env python
"""
Redownload asset files.

"""

import os
import shutil
import subprocess
import sys
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
    "bootstrap-3.1.0.min.css": "https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css",
    "stupidtable.js": "https://github.com/joequery/Stupid-Table-Plugin/raw/1.0.1/stupidtable.js",
    "jquery.flot.axislabels.js": "https://github.com/xuanluo/flot-axislabels/raw/master/jquery.flot.axislabels.js",
    "jquery.flot.orderBars.js": "https://www.benjaminbuffet.com/public/js/jquery.flot.orderBars.js",
    "md5.js": "https://cdnjs.cloudflare.com/ajax/libs/blueimp-md5/2.10.0/js/md5.js",
}

LICENSE_FILES = {
    "stupidtable.js": "https://github.com/joequery/Stupid-Table-Plugin/raw/1.0.1/LICENSE",
    "jquery.flot-0.8.2.min.js": "https://github.com/flot/flot/raw/v0.8.2/LICENSE.txt",
    "jquery.flot-0.8.2.time.min.js": "https://github.com/flot/flot/raw/v0.8.2/LICENSE.txt",
    "jquery.flot-0.8.2.selection.min.js": "https://github.com/flot/flot/raw/v0.8.2/LICENSE.txt",
    "jquery.flot-0.8.2.categories.min.js": "https://github.com/flot/flot/raw/v0.8.2/LICENSE.txt",
}

VENDOR_DIR = os.path.abspath(os.path.dirname(__file__))


def download_assets():
    if not os.path.isdir(VENDOR_DIR):
        os.makedirs(VENDOR_DIR)

    for fn, asset in sorted(VENDOR_ASSETS.items()):
        dst = os.path.join(VENDOR_DIR, fn)

        if os.path.isfile(dst):
            continue

        if fn in LICENSE_FILES:
            license_asset = LICENSE_FILES[fn]

            print("Downloading {0} into {1}...".format(license_asset, fn))

            fsrc = urlopen(LICENSE_FILES[fn])
            try:
                with open(dst + ".new", "wb") as fdst:
                    fdst.write('/*\n')
                    shutil.copyfileobj(fsrc, fdst)
                    fdst.write('*/\n\n'.format(license_asset))
            finally:
                fsrc.close()
            mode = 'ab'
        else:
            mode = 'wb'

        print("Downloading {0} to {1}...".format(asset, fn))

        fsrc = urlopen(asset)
        try:
            with open(dst + ".new", mode) as fdst:
                shutil.copyfileobj(fsrc, fdst)
        finally:
            fsrc.close()

        patch = dst + '.patch'
        if os.path.isfile(patch):
            # Patch
            subprocess.check_call(['patch', dst + '.new', patch])

        # Usually atomic
        os.rename(dst + ".new", dst)


if __name__ == "__main__":
    download_assets()
