#! /usr/bin/env python3

import argparse

from utils import working_directory
from utils import os_install
from utils import python2_install
from utils import python3_install
from utils import exec_cmd


def main(elevate=False, ros_init=False, create_ws=False):

    pre = 'sudo' if elevate else ''
    pre_python = 'sudo -H' if elevate else ''

    os_install(*UBUNTU18_PACKAGES, pre=pre)

    if ros_init:
        initialize_ros(pre=pre)

    os_install(*ROS_MELODIC_PACKAGES, pre=pre)

    if ros_init:
        initialize_rosdep(pre=pre)

    python2_install(*PYTHON_PACKAGES, pre=pre_python)
    python3_install(*PYTHON_PACKAGES, pre=pre_python)

    if create_ws:
        create_workspace()


def initialize_ros(pre=''):
    set_up_src_list_cmd = ['sh', '-c', 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" '
                                       '> /etc/apt/sources.list.d/ros-latest.list']
    set_up_key_cmd = ['apt-key', 'adv', '--keyserver', 'hkp://keyserver.ubuntu.com:80',
                      '--recv-key', 'C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654']

    if pre:
        set_up_src_list_cmd = [pre] + set_up_src_list_cmd
        set_up_key_cmd = [pre] + set_up_key_cmd
#
    exec_cmd(set_up_src_list_cmd)
    exec_cmd(set_up_key_cmd)


def initialize_rosdep(pre=''):
    exec_cmd('{pre} rosdep init', pre=pre)
    exec_cmd('rosdep update')


def create_workspace():
    exec_cmd('mkdir -p /root/melo_ws/src')

    with working_directory('/root/melo_ws/src'):
        exec_cmd('git clone https://github.com/ros-planning/moveit_tutorials.git -b melodic-devel')
        exec_cmd('git clone https://github.com/ros-planning/panda_moveit_config.git -b melodic-devel')
        exec_cmd('rosdep install -y --from-paths . --ignore-src --rosdistro melodic')

    with working_directory('/root/melo_ws'):
        exec_cmd('catkin config --extend /opt/ros/melodic --cmake-args -DCMAKE_BUILD_TYPE=Release')
        exec_cmd('catkin build')


UBUNTU18_PACKAGES = [
    'apt-utils',
    'lsb-core',
    'build-essential',
    'ninja-build',
    'pkg-config',
    'gnupg2',
    'git',
    'sudo',
    'gcc',
    'g++',
    'gdb',
    'clang',
    'cmake',
    'rsync',
    'tar',
    'python-dev',
    'python3-dev',
    'unzip',
    'ffmpeg',
    'qt5-default',
    'qtbase5-dev',
    'nano',
    'vim',
    'qt5-qmake',
    'python-numpy',
    'python3-numpy',
    'libopencv-dev',
    'libgtk-3-dev',
    'libjpeg-dev',
    'libpng-dev',
    'libprotobuf-dev',
    'protobuf-compiler',
    'libtiff5-dev',
    'libavcodec-dev',
    'libavformat-dev',
    'libswscale-dev',
    'libgoogle-glog-dev',
    'libgflags-dev',
    'libhdf5-dev',
    'doxygen',
    'libgstreamer-gl1.0-0',
    'libgstreamer-plugins-base1.0-dev',
    'yasm',
    'libboost-all-dev',
    'gfortran',
    'libtheora-dev',
    'libxvidcore-dev',
    'v4l-utils',
    'liblapacke-dev',
    'libopenblas-dev',
    'libgdal-dev',
    'checkinstall',
    'libgl1-mesa-dev',
    'mesa-utils',
    'wayland-protocols',
    'libavdevice-dev',
    'libglew-dev',
    'libatlas-base-dev',
    'liblapack-dev',
    'libsuitesparse-dev',
    'python3-pip',
    'python3-opencv',
    'python-pip',
    'python-opencv',
    'libeigen3-dev',
    'xterm',
    'gedit',
    'wget',
    'python-tk',
]


ROS_MELODIC_PACKAGES = [
    'ros-melodic-desktop-full',
    'python-rosdep',
    'ros-melodic-catkin',
    'python-catkin-tools',
    'ros-melodic-moveit',
]


PYTHON_PACKAGES = [
    'numpy',
    'Pillow',
    'pybind11',
    'matplotlib',
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--elevate', action='store_true',
                        help='If specified, commands that need sudo will require it.'
                             'Do not use it if you are root. Use it otherwise.')
    parser.add_argument('-r', '--ros_init', action='store_true',
                        help='If specified, sources.list and keys for ROS melodic '
                             'will be set up')
    parser.add_argument('-w', '--create_ws', action='store_true',
                        help='If specified, creates catkin workspace')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(elevate=args.elevate, ros_init=args.ros_init, create_ws=args.create_ws)
