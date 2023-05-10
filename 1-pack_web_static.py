#!/usr/bin/python3
""" This script generates a .tgz archive from the web_static folder """
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Generates a .tgz archive from the web static folder"""

    time = datetime.now()
    time = time.strftime("%Y%m%d%H%M%S")
    filename = "web_static_{}.tgz".format(time)
    archive_path = "versions/{}".format(filename)

    print("Packing web_static to {}".format(archive_path))

    local("mkdir -p versions")
    local("tar -cvzf {} web_static".format(archive_path))

    print("Successfully packed web_static to {}".format(archive_path))

    return archive_path
