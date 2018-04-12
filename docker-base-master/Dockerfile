FROM centos:6.4
MAINTAINER acoyle <acoyle@powa.com>

RUN yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum -y update
RUN yum -y install pwgen bash-completion openssh-server psmisc net-tools sudo rsyslog

RUN useradd -G wheel user

# Would prefer to use mock instead of rpmbuild, but it doesn't seem to work in a Docker container
RUN yum -y install rpmdevtools yum-utils
RUN yumdownloader --source supervisor
RUN yum-builddep -y --nogpgcheck supervisor-2.1-8.el6.src.rpm
RUN yum -y install python-setuptools
RUN su - user -c "rpmdev-setuptree && rpm -ivh /supervisor-2.1-8.el6.src.rpm"
RUN su - user -c "cd ~/rpmbuild/SOURCES && wget -q --no-check-certificate http://pypi.python.org/packages/source/s/supervisor/supervisor-3.0.tar.gz"
ADD ./supervisor/supervisord.conf.f20 /home/user/rpmbuild/SOURCES/supervisord.conf
RUN chown user:user ~user/rpmbuild/SOURCES/supervisord.conf
ADD ./supervisor/supervisor.spec /home/user/rpmbuild/SPECS/supervisor.spec
RUN chown user:user ~user/rpmbuild/SPECS/supervisor.spec
RUN su - user -c "cd ~/rpmbuild/SPECS && rpmbuild -ba supervisor.spec"
RUN yum -y history rollback last-3
RUN yum -y localinstall ~user/rpmbuild/RPMS/noarch/supervisor-3.0-1.el6.noarch.rpm

ADD ./supervisor/sshd.ini /etc/supervisord.d/sshd.ini
ADD ./supervisor/rsyslogd.ini /etc/supervisord.d/rsyslogd.ini

RUN mkdir /var/run/sshd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
#RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
#RUN sed -ri 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config
#RUN echo "ClientAliveInterval 60" | tee -a /etc/ssh/sshd_config

RUN chmod u+w /etc/sudoers
RUN sed -ri $'s/# %wheel\tALL=\(ALL\)\tALL/%wheel\t\tALL=(ALL)\tALL/g' /etc/sudoers
RUN chmod u-w /etc/sudoers

ADD ./start.sh /start.sh
RUN chmod 755 /start.sh

# EXPOSE 22

CMD ["/bin/bash", "/start.sh"]
