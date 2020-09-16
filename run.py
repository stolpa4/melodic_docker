#! /usr/bin/env python3

import os
import json
from pathlib import Path
import argparse

from utils import working_directory
from utils import exec_cmd
from utils import CalledProcessError


DOCKER_STOP_CMD_FMT = 'docker stop {container_id}'
DOCKER_RM_CMD_FMT = 'docker rm {container_id}'
DOCKER_RUN_CMD_FMT = ('{pre} docker run -dit --privileged --cap-add=ALL '
                      '-v /tmp/.X11-unix:/tmp/.X11-unix --gpus all '
                      '--name {container_id} '
                      f'-e DISPLAY={os.environ["DISPLAY"]} '
                      f'-e XAUTHORITY={os.environ["XAUTHORITY"]} '
                      '{additional_flags} '
                      '{image_name}')


def main(args):
    mount_flags = get_mount_dirs_str(args.mount)

    if args.stop_rm:
        stop_rm_container(args.container_id)

    with working_directory(path=Path(__file__).parent):
        exec_cmd('xhost +local:docker')

        exec_cmd(DOCKER_RUN_CMD_FMT, pre='sudo' if args.elevate else '',
                 container_id=args.container_id,
                 additional_flags=mount_flags,
                 image_name=get_image_name(args.image_name))


def stop_rm_container(container_id):
    try:
        exec_cmd(DOCKER_STOP_CMD_FMT, container_id=container_id)
    except CalledProcessError:
        pass
    try:
        exec_cmd(DOCKER_RM_CMD_FMT, container_id=container_id)
    except CalledProcessError:
        pass


def get_image_name(name):
    if name:
        return name

    try:
        name = json.load(open('.build.meta'))['image_name']
    except FileNotFoundError:
        raise NoBuildMetaInformationFoundError()

    return name


class NoBuildMetaInformationFoundError(Exception):
    def __init__(self):
        msg = ('Unable to run an image as no build meta information file found!'
               'Please, build the container with ./build command or provide the --image_name option.')
        super().__init__(msg)


def get_mount_dirs_str(mount_list):
    return ' '.join(f'-v {Path(mnt).resolve()}:/root/{Path(mnt).resolve().name}' for mnt in mount_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--image_name', default='',
                        help='Name of the built Docker image. By default the name '
                             'used in "build.py" command will be loaded')
    parser.add_argument('-i', '--container_id', default='ros_melodic1',
                        help='ID of the run container')
    parser.add_argument('-m', '--mount', nargs='+', default=['../'],
                        help='Mount directories. You can specify multiple paths, '
                             'separating them by a whitespace. All specified directories will '
                             'be mounted to /root/<leaf_directory_name>')
    parser.add_argument('-e', '--elevate', action='store_true',
                        help='If specified, commands that need sudo will require it.'
                             'Do not use it if you are root, or if '
                             'you are in the docker group. Use it otherwise.')
    parser.add_argument('-s', '--stop_rm', action='store_true',
                        help='Try to stop and remove a container with the same conteiner id')
    main(parser.parse_args())
