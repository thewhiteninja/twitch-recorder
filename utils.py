import errno
import os
import platform
import subprocess
import sys
import time
from datetime import datetime
from packaging import version


def check_streamlink_version(minimal_version="5.1.0"):
    v = subprocess.check_output(["streamlink", "-V"], timeout=5).decode().strip()
    return version.parse(v[11:]) >= version.parse(minimal_version)


def log(s):
    d = datetime.now()
    sys.stdout.write("%s - %s\n" % (d.strftime("%m/%d/%Y %H:%M:%S"), s))
    sys.stdout.flush()


def make_directory(dir_path):
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                return False
    return True


def change_extension(f, ext):
    base = os.path.splitext(f)[0]
    os.rename(f, base + ext)


def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if nbytes == 0:
        return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    if nbytes - int(nbytes) > 0.0:
        return '%.2f %s' % (nbytes, suffixes[i])
    else:
        return '%d %s' % (nbytes, suffixes[i])


def welcome():
    print("Starting %s at %s (%s version)\n" % (
        os.path.basename(sys.argv[0]), time.asctime(time.localtime(time.time())), platform.architecture()[0]))
