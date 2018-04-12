docker-base
========================

Tested on Docker 0.9.0

This repo contains a recipe for making a base Docker image with SSH and SYSLOG on CentOS.

Check your Docker version

\# docker version

Perform the build

\# docker build -rm -t <yourname>/docker-base .

Check the image out.

\# docker images

Run it:

\# docker run -d -p 22:22 <yourname>/docker-base

(Note, port mapping is only required if remote access is required)

Get container ID:

\# docker ps

Keep in mind the user password set for ssh is automatically generated.

Get the user password by inspecting the logs:

\# docker logs <container_id>

Get the IP address for the container:

\# docker inspect <container_id> | grep -i ipaddr

For SSH:
\# ssh user@172.17.0.x

