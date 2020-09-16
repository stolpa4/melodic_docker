#! /usr/bin/env python3

import sys
from pathlib import Path
import json

from utils import working_directory
from utils import exec_cmd


CUR_DIR = Path(__file__).parent
DOCKER_BUILD_CMD_FMT = 'docker build -t {img_name} -f Dockerfile .'


def main(image_name):
    with working_directory(path=Path(__file__).parent):
        build(image_name)
        save_meta_info(image_name)


def build(img_name):
    exec_cmd(DOCKER_BUILD_CMD_FMT, img_name=img_name)


def save_meta_info(img_name):
    with open('.build.meta', 'w') as f:
        json.dump({'image_name': img_name}, f, indent=4)


def parse_args():
    default_name = 'ros_melodic'

    if len(sys.argv) == 1:
        img_name = default_name
    elif len(sys.argv) == 2:
        img_name = sys.argv[1]
    else:
        print("Usage: ./build [image_name]. "
              f"Default name: {default_name}")
        exit(1)

    validate_name(img_name)

    return img_name


def validate_name(img_name):
    if not img_name.isidentifier():
        print("The name specified is not a valid python identifier")
        exit(2)

    return True


if __name__ == '__main__':
    main(parse_args())
