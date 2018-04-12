%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(
)")}
Summary:  A System for Allowing the Control of Process State on UNIX
Name: supervisor
Version: 3.0
Release: 1%{?dist}

License: ZPLv2.1 and BSD and MIT
Group: System Environment/Base
URL: http://supervisord.org/
Source: http://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}%{?prever}.tar.gz
Source1: supervisord.init
Source2: supervisord.conf
Source3: supervisor.logrotate
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-setuptools

Requires: python-meld3 >= 0.6.5
Requires: python-setuptools
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service, /sbin/chkconfig


%description
The supervisor is a client/server system that allows its users to control a
number of processes on UNIX-like operating systems.

%prep
%setup -q

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/supervisord.d
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/logrotate.d/
%{__mkdir} -p %{buildroot}/%{_initrddir}
%{__mkdir} -p %{buildroot}/%{_localstatedir}/log/%{name}
%{__chmod} 770 %{buildroot}/%{_localstatedir}/log/%{name}
%{__install} -p -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/supervisord
%{__install} -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/supervisord.conf
%{__install} -p -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/supervisor
%{__sed} -i s'/^#!.*//' $( find %{buildroot}/%{python_sitelib}/supervisor/ -type f)

%{__rm} -rf %{buildroot}/%{python_sitelib}/supervisor/meld3/

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}d || :

%preun
if [ $1 = 0 ]; then
    /sbin/service supervisord stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}d || :
fi

%files
%defattr(-,root,root,-)
%doc CHANGES.txt COPYRIGHT.txt README.rst LICENSES.txt PLUGINS.rst TODO.txt
%dir %{_localstatedir}/log/%{name}
%{_initrddir}/supervisord
%{python_sitelib}/*
%{_bindir}/supervisor*
%{_bindir}/echo_supervisord_conf
%{_bindir}/pidproxy

%config(noreplace) %{_sysconfdir}/supervisord.conf
%dir %{_sysconfdir}/supervisord.d
%config(noreplace) %{_sysconfdir}/logrotate.d/supervisor

%changelog
* Mon Mar 24 2012 Alex Coyle <acoyle@powa.com> - 3.0-1
- Rebuild for Supervisor 3.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1-6
- Rebuild for Python 2.6

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1-5
- fix license tag

* Mon Jan 07 2008 Toshio Kuratomi <toshio@fedoraproject.org>  2.1-4
- Include egginfo files when python generates them.

* Sun Apr 22 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-3
- Added BuildRequires of python-devel

* Fri Apr 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-2
- Added patch suggested in #153225

* Fri Apr 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-1
- Initial packaging

