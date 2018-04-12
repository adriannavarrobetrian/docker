#!/bin/bash -eux

# Enable EPEL repo

yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

# Install Ansible 2.0 compiled RPM

yum -y install /tmp/ansible-2.0.2.0-1.el6.noarch.rpm

# Install cloud-init for launch scripts

yum -y install cloud-init dracut-modules-growroot cloud-utils-growpart telnet

rpm -qa kernel | sed 's/^kernel-//'  | xargs -I {} dracut -f /boot/initramfs-{}.img {}

# Update OS - DISABLED

#yum -y update 

# Make Ansible pass dir 

mkdir -p /etc/ansible/pass
