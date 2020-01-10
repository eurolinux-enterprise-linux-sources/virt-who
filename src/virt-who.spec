Name:           virt-who
Version:        0.12
Release:        1%{?dist}
Summary:        Agent for reporting virtual guest IDs to subscription-manager

Group:          System Environment/Base
License:        GPLv2+
URL:            https://fedorahosted.org/virt-who/
Source0:        https://fedorahosted.org/releases/v/i/virt-who/%{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       libvirt-python
# python-rhsm 1.10.10 has required call for guestId support
Requires:       python-rhsm >= 1.10.10
# python-suds is required for vSphere support
Requires:       python-suds
# m2crypto is required for Hyper-V support
Requires:       m2crypto
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description
Agent that collects information about virtual guests present in the system and
report them to the subscription manager.

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/virt-who.d
touch %{buildroot}/%{_sharedstatedir}/%{name}/key

# Don't run test suite in check section, because it need the system to be
# registered to subscription-manager server

%clean
rm -rf $RPM_BUILD_ROOT

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add virt-who

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service virt-who stop >/dev/null 2>&1
    /sbin/chkconfig --del virt-who
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service virt-who condrestart >/dev/null 2>&1 || :
fi


%files
%doc README LICENSE
%{_bindir}/virt-who
%{_bindir}/virt-who-password
%{_datadir}/virt-who/
%{_sysconfdir}/rc.d/init.d/virt-who
%attr(600, root, root) %dir %{_sysconfdir}/virt-who.d
%attr(600, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/virt-who
%{_mandir}/man8/virt-who.8.gz
%{_mandir}/man8/virt-who-password.8.gz
%{_mandir}/man5/virt-who-config.5.gz
%attr(600, root, root) %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/key


%changelog
* Fri Feb 27 2015 Radek Novacek <rnovacek@redhat.com> 0.12-1
- Version 0.12

* Mon Sep 08 2014 Radek Novacek <rnovacek@redhat.com> 0.11-1
- Version 0.11

* Tue May 20 2014 Radek Novacek <rnovacek@redhat.com> 0.10-1
- Add directory with configuration files
- Version 0.10

* Thu Mar 13 2014 Radek Novacek <rnovacek@redhat.com> 0.9-1
- Remove libvirt dependency
- Add dependency on m2crypto
- Version 0.9

* Fri Sep 14 2012 Radek Novacek <rnovacek@redhat.com> 0.8-1
- Version 0.8

* Mon Jul 09 2012 Radek Novacek <rnovacek@redhat.com> 0.7-1
- Version 0.7

* Mon Feb 13 2012 Radek Novacek <rnovacek@redhat.com> 0.6-1
- Version 0.6

* Fri Dec 09 2011 Radek Novacek <rnovacek@redhat.com> 0.5-1
- VSphere support
- Req: python-suds

* Wed Nov 30 2011 Radek Novacek <rnovacek@redhat.com> 0.4-1
- Version 0.4

* Thu Oct 06 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-2
- Requires python-rhsm >= 0.96.13 (contains fix for char limit in uuid list)

* Thu Sep 01 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-1
- Add initscript and configuration file

* Mon Aug 22 2011 Radek Novacek <rnovacek@redhat.com> - 0.2-1
- Update to upstream version 0.2
- Add Requires: libvirt

* Fri Aug 19 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-2
- Add BuildRoot tag (the package will be in RHEL5)

* Wed Aug 10 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-1
- initial import
