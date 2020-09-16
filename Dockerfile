FROM nvidia/opengl:base-ubuntu18.04

COPY install_dependencies.py /tmp
COPY utils.py /tmp

ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib

RUN apt update && apt install -y python3
RUN chmod +x /tmp/install_dependencies.py && /tmp/install_dependencies.py --ros_init --create_ws
RUN yes 1234 | passwd root

RUN touch /root/setup.sh
RUN echo 'source /opt/ros/melodic/setup.bash' >> /root/setup.sh
RUN echo 'source /root/melo_ws/devel/setup.bash' >> /root/setup.sh

ENTRYPOINT /bin/bash