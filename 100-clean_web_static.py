#!/usr/bin/python3
""" This script deploys an archive to servers"""
from fabric.api import local, put, run, env, runs_once
from datetime import datetime
from os.path import isfile


env.user = "ubuntu"
env.hosts = ["34.232.52.43", "54.175.12.49"]


@runs_once
def do_pack():
    """ Generates a .tgz archive """

    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "web_static_{}.tgz".format(time_now)
    archive_path = "versions/{}".format(filename)
    local("mkdir -p versions")
    local("tar -cvzf {} web_static".format(archive_path))

    return archive_path


def do_deploy(archive_path):
    """ Deploys an archive to server """

    if not isfile(archive_path):
        return False

    archive_name = archive_path.split("/")[-1]
    folder_name = archive_name[: -4]
    dir_path = "/data/web_static/releases/{}".format(folder_name)

    put(archive_path, "/tmp/")
    run("mkdir -p {}".format(dir_path))
    run("tar -xzf /tmp/{} -C {}".format(archive_name, dir_path))
    run("cp -r {}/web_static/* {}".format(dir_path, dir_path))
    run("rm -rf /tmp/{} {}/web_static".format(archive_name, dir_path))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(dir_path))


    return True


def deploy():
    """ Performs a full deployment"""

    filename = do_pack()
    if not filename:
        return False

    return do_deploy(filename)


@runs_once
def clean_local(number=0):
    """ local cleanup """

    versions = local("ls versions", capture=True).split("\n")

    number = int(number)
    if number == 0:
        vers_to_keep = 1
    else:
        vers_to_keep = number

    vers_to_del = versions[: -vers_to_keep]
    if len(vers_to_del) == 0:
        return

    for i in range(len(vers_to_del)):
        vers_to_del[i] = "versions/" + vers_to_del[i]

    vers_to_del = " ".join(vers_to_del)

    local("rm {}".format(vers_to_del))


def clean_server(number=0):
    """ cleanup server """

    versions = run("ls /data/web_static/releases | grep web_static")
    versions = versions.stdout.split("\n")

    number = int(number)
    if number == 0:
        vers_to_keep = 1
    else:
        vers_to_keep = number

    vers_to_del = versions[: -vers_to_keep]
    if len(vers_to_del) == 0:
        return

    for i in range(len(vers_to_del)):
        vers_to_del[i] = vers_to_del[i].strip()
        vers_to_del[i] = "/data/web_static/releases/" + vers_to_del[i]

    vers_to_del = " ".join(vers_to_del)
    run("sudo rm -rf {}".format(vers_to_del))


def do_clean(number=0):
    """ Performs cleanup action """

    clean_local(number)
    clean_server(number)
