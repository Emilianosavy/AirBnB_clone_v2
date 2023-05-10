#!/usr/bin/python3
""" This script deploys an archive"""
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import isfile

env.user = "ubuntu"
env.hosts = ["34.232.52.43", "54.175.12.49"]


def do_pack():
    """ Generates a .tgz archive """

    time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "web_static_{}.tgz".format(time)
    archive_path = "versions/{}".format(filename)

    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.failed:
        return None

    return archive_path


def do_deploy(archive_path):
    """ Deploys an archive to webserver """

    if not isfile(archive_path):
        return False

    archive_name = archive_path.split("/")[-1]
    folder_name = archive_name[: -4]
    dir_path = "/data/web_static/releases/{}".format(folder_name)

    put(archive_path, "/tmp/")
    run("mkdir -p {}".format(dir_path))
    result = run("tar -xzf /tmp/{} -C {}".format(archive_name, dir_path))

    if result.failed:
        return False

    run("cp -r {}/web_static/* {}".format(dir_path, dir_path))
    run("rm -rf /tmp/{} {}/web_static".format(archive_name, dir_path))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(dir_path))

    return True
