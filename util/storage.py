import errno
import os
import os.path
import pathlib


def set_storage_directory():
    user_home = os.path.expanduser("~/") # Thanks to @susam
    dir = os.path.join(user_home, ".qry")
    d = pathlib.Path(dir)
    if d.exists() and not d.is_dir():
        sys.stderr.write("A file already exists that does not belong to QRy\n")
        sys.stderr.flush()
        return errno.EEXIST

    if not d.exists():
        os.mkdir(dir, mode=0o0760)

    return 0

def get_storage_directory():
    user_home = os.path.expanduser("~/")
    return os.path.join(user_home, ".qry")

def get_default_config_path():
    return os.path.join(get_storage_directory(), "qry.json")
