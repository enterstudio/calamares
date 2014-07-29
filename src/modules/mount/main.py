#!/usr/bin/env python3
# encoding: utf-8
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014, Aurélien Gâteau <agateau@kde.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess
import tempfile

import libcalamares


# FIXME: Duplicated between mount and grub
def mount(device_path, mount_point, fs=None, options=None):
    assert device_path
    assert mount_point
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)
    cmd = ["mount", device_path, mount_point]
    if fs:
        cmd += ("-t", fs)
    if options:
        cmd += ("-o", options)
    subprocess.check_call(cmd)


def mount_partitions(root_mount_point, partitions):
    for partition in partitions:
        if not partition["mountPoint"]:
            continue
        # Create mount point with `+` rather than `os.path.join()` because
        # `partition["mountPoint"]` starts with a '/'.
        mount_point = root_mount_point + partition["mountPoint"]
        mount(partition["device"], mount_point,
              fs=partition.get("fs"),
              options=partition.get("options")
              )


def run():
    root_mount_point = tempfile.mkdtemp(prefix="calamares-root-")
    partitions = libcalamares.globalstorage.value("partitions")

    # Sort by mount points to ensure / is mounted before the rest
    partitions.sort(key=lambda x: x["mountPoint"])
    mount_partitions(
        root_mount_point, libcalamares.globalstorage.value("partitions"))

    libcalamares.globalstorage.insert("rootMountPoint", root_mount_point)
    return None
