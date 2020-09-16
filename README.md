Easy ROS melodic container
==========================

About
-----
These scripts are there for easy building and running a ROS melodic container with OpenGL support. You can use your favorite tools like RViZ or Gazebo from this container seamlessly.


Prerequisites
-------------
To be able to use this stuff, you need to have several things set up:
    
   1. Dedicated Nvidia GPU (the only supported option for now).
   2. Ubuntu 18.04+ or Debian 9+
   3. Properly installed drivers for the GPU
   4. Properly installed [Docker](https://www.docker.com/)
   5. Properly installed [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) (the package name is `nvidia-docker2`. Don't forget tor restart the docker service after installation)
   6. A python3 executable (only standard library is required).

Also make sure you've [added your user to the `docker` group](https://docs.docker.com/engine/install/linux-postinstall/).

Windows
-------
Hopefully, it is possible to run these scripts in Windows (maybe some minor changes needed). You also need an [X-server](https://sourceforge.net/projects/xming/) to be installed (don't forget to run it).

Warning
-------
The project was tested in Ubuntu 18.04 and Ubuntu 20.04 only. Sorry for that.
In this (and in every other) regard contributions are strongly encouraged.

Usage
-----
Again, please, make sure your current user is in the `docker` group.

### 1. Build the container
You can build the container by using these commands.
``` bash
chmod +x build.py
./build.py
```
Or simply put `python3 build.py`.

The `build.py` script has one optional positional argument: `image_name`. It is simply the name of the image to be created. The **default image name** is: `ros_melodic`.

The `build.py` script will save the image name in use to a `.build.meta` file in JSON format. This is done to let the other script, namely `run.py` to be used without user-provided arguments (by default, `run.py` will extract the image name from the `.build.meta` file).

After building you get an image with `ros-melodic-desktop-full` and `ros-melodic-moveit` packages installed. Also some other basic developer tools are installed. The container has a ROS workspace `/root/melo_ws` with `moveit_tutorials` and `panda_moveit_config` prebuilt packages. 

### 2. Run the container
To run the built image, simply put:

``` bash
chmod +x run.py
./run.py
```

Or similarly, `python3 run.py`.
The `run.py` script has several command-line options. They are described below.

#### -n, --image_name <name>
Name of the built Docker image. By default the name used in the `build.py` command will be loaded (from `.build.meta` file mentioned above). Feel free to provide any image name you think is appropriate by using this option.

#### -i, --container_id <id>
The container ID, i.e. a name to attach to the container on run. The default name is: `ros_melodic1`. 

Be careful, if there exists a container with the same name, the script will issue a error. You need to `stop` the old container and `rm` it, otherwise consider using `-s` flag (described below) or provide other container_id to avoid name collisions.

#### -m --mount path1 [path2 [...]]
Path(s) to be mounted in the container. By default, only the upper-level parent directory of the `run.py` script is mounted. However you can provide your own path (or several paths, separated by a whitespace), either absolute or relative.
All the paths provided will be mounted into the `/root/<leaf_directory_name_of_the_path>` folder.

#### -s --stop_rm
Try to stop and remove a container with the same container_id, that provided to the script. If there is no container with that id, the script will issue couple of errors, but eventually will finish its job, so just ignore those.

### 3. Start working with the container
From the terminal run `docker attach <container_id>` (the default container id is `ros_melodic1`). After that run `source /root/setup.sh` to set up the ROS environment. And then you can spawn terminals and work with ROS. To spawn a terminal, simply put: `xterm &`. The spawned terminals will inherit the host terminal environment, so there is no need to run `/root/setup.sh` in any of them.

The install_dependencies.py script
----------------------------------
The script can be used from Ubuntu 18.04 system and is used by the docker during the building procedure (from within a container).

So, normally you will not use this script, as it is used automatically. But if you want to install the ROS system-wide on your machine (together with some other useful stuff) - you are welcome.

It installs dependencies as well as some basic developer tools, optionally sets up ROS repository, key and workspace.

The arguments of this script are listed below.

#### -e --elevate
This argument is almost always needed if you use this script by hand. It provides your permission to use sudo (to install packages with apt, system-wide). Do not use this flag if you are root.

#### -r --ros_init
Use this argument to set up ros repository and key.

#### -w --create_ws
Use this argument to create a ROS workspace `/root/melo_ws` with moveit tutorials prebuilt.


Troubleshooting
---------------
Please, create an issue. I will try to respond to it ASAP.