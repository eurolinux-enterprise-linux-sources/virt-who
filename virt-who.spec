Name:           virt-who
Version:        0.16
Release:        8%{?dist}
Summary:        Agent for reporting virtual guest IDs to subscription-manager

Group:          System Environment/Base
License:        GPLv2+
URL:            https://fedorahosted.org/virt-who/
Source0:        https://fedorahosted.org/releases/v/i/virt-who/%{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       libvirt-python
# python-rhsm 1.10.10 has support for sending additional information together with guest uuids
Requires:       python-rhsm >= 1.10.10
# python-suds is required for vSphere support
Requires:       python-suds
# m2crypto is required for Hyper-V support
Requires:       m2crypto
Requires:       python-requests
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts


# Fix typo in template.conf
Patch0:         virt-who-0.16-fix-typo-in-template-conf.patch
# HyperV: support ntlm sealing and signing
Patch1:         virt-who-0.16-hyperv-support-ntlm-sealing.patch
# Use whole report as argument to hypervisorCheckIn and sendVirtGuests
Patch2:         virt-who-0.16-use-whole-report-for-hypervisorCheckIn.patch
# Refactor main loop and job scheduling
Patch3:         virt-who-0.16-refactor-main-loop-and-jobs.patch
# Improve logging
Patch4:         virt-who-0.16-improve-logging.patch
# Better handling of 429 error code
Patch5:         virt-who-0.16-better-handling-of-429.patch
# Background and oneshot modes are no longer exclusive
Patch6:         virt-who-0.16-background-and-oneshot-not-exclusive.patch
# Handle unregister gracefully
Patch7:         virt-who-0.14-handle-unregister-gracefully.patch
# Documentation and manual page fixes
Patch8:         virt-who-0.14-docu-and-manpage-fixes.patch
# Don't terminate virt-who if the system is not registered
Patch9:         virt-who-0.16-dont-terminate-when-unregistered.patch
# Reword note about hwuuid in man page
Patch10:        virt-who-0.16-reword-hwuuid-note-in-manpage.patch
# Change pidfile permissions to 600
Patch11:        virt-who-0.16-pidfile-permission-600.patch
# Do not change minimal reporting interval by interval option
Patch12:        virt-who-0.16-no-minimal-interval-change.patch
# Fix default interval in the man page
Patch13:        virt-who-0.16-fix-default-interval-man-page.patch
# No rate limit for first round of updates
Patch14:        virt-who-0.16-no-rate-limit-for-first-updates.patch
# Honor interval even with event monitoring
Patch15:        virt-who-0.16-honor-interval-with-event-monitoring.patch
# Fix satellite5 env var usage
Patch16:        virt-who-0.16-satellite5-fix-env-var-usage.patch
# Don't print anything when nothing found in the print mode
Patch17:        virt-who-0.16-dont-print-when-nothing-found.patch
# Handle no hostname returned from esx
Patch18:        virt-who-0.16-handle-no-hostname-returned-from-esx.patch
# ESX: fix logging out from hypervisor on exit
Patch19:        virt-who-0.16-esx-fix-logging-out-from-hypervisor.patch
# VDSM: do not enforce sslv3
Patch20:        virt-who-0.16-dont-enforce-sslv3.patch


%description
Agent that collects information about virtual guests present in the system and
report them to the subscription manager.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1


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
%doc README.md README.hyperv LICENSE
%{_bindir}/virt-who
%{_bindir}/virt-who-password
%{_datadir}/virt-who/
%{_sysconfdir}/rc.d/init.d/virt-who
%{_sysconfdir}/virt-who.conf
%attr(700, root, root) %dir %{_sysconfdir}/virt-who.d
%{_sysconfdir}/virt-who.d/template.conf
%attr(600, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/virt-who
%{_mandir}/man8/virt-who.8.gz
%{_mandir}/man8/virt-who-password.8.gz
%{_mandir}/man5/virt-who-config.5.gz
%attr(700, root, root) %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/key


%changelog
* Thu Mar 31 2016 Radek Novacek <rnovacek@redhat.com> 0.16-8
- ESX: fix logging out from hypervisor on exit
- VDSM: do not enforce sslv3
- Resolves: rhbz#1249928

* Thu Mar 10 2016 Radek Novacek <rnovacek@redhat.com> 0.16-7
- Fix satellite5 env var usage
- Don't print anything when nothing found in the print mode
- Handle no hostname returned from esx
- Resolves: rhbz#1284037

* Thu Feb 25 2016 Radek Novacek <rnovacek@redhat.com> 0.16-6
- No rate limit for first round of updates
- Honor interval even with event monitoring
- Resolves: rhbz#1230041, rhbz#1295644

* Tue Feb 23 2016 Radek Novacek <rnovacek@redhat.com> 0.16-5
- Change pidfile permissions to 600
- Do not change minimal reporting interval by interval option
- Fix default interval in the man page
- Resolves: rhbz#1310977

* Thu Feb 11 2016 Radek Novacek <rnovacek@redhat.com> 0.16-4
- Don't terminate virt-who if the system is not registered
- Reword note about hwuuid in man page
- Resolves: rhbz#1293821, rhbz#1233074

* Tue Feb 02 2016 Radek Novacek <rnovacek@redhat.com> 0.16-3
- Requires: python-requests
- Resolves: rhbz#1294746

* Tue Jan 26 2016 Radek Novacek <rnovacek@redhat.com> 0.16-2
- Support NTLM sealing
- Fix interval issues
- Improve exception handling
- Make background and oneshot modes not exclusive
- Handle unregister gracefully
- Documentation and manual page fixes
- Resolves: rhbz#1294746

* Thu Dec 17 2015 Radek Novacek <rnovacek@redhat.com> 0.16-1
- Rebase to virt-who-0.16
- Resolves: rhbz#1258765

* Thu Jun 04 2015 Radek Novacek <rnovacek@redhat.com> 0.12-10
- Esx: handle vcenter restart
- subscriptionmanager: suppress BadStatusLine exception
- Resolves: rhbz#1208345

* Tue May 26 2015 Radek Novacek <rnovacek@redhat.com> 0.12-9
- Fake: fix loading data from file as utf-8
- Clear the queue before putting exit/reload there
- rhevm: don't throw an exception when host doesn't have hardware uuid
- log: don't rotate log file, it already has logrotate
- libvirtd: properly terminate libvirt connection on exit
- Resolves: rbhz#1223647

* Thu May 14 2015 Radek Novacek <rnovacek@redhat.com> 0.12-8
- Fix virt backend termination
- esx: report host/guest assoc even if empty
- Limit queue size to number of virt backends
- rhevm: don't fail when hwuuid is not present
- Show error when encrypted password is corrupted
- Resolves: rhbz#1215007

* Tue May 05 2015 Radek Novacek <rnovacek@redhat.com> 0.12-7
- Fix oneshot mode for multiple hypervisors
- Fake: load the data from file as utf-8
- Add a note that changing hypervisor_id will result in duplicated entries
- Terminate background processes when main process exits
- Log the result in print mode
- Resolves: rhbz#1215007

* Thu Apr 23 2015 Radek Novacek <rnovacek@redhat.com> 0.12-6
- Stop backends when system is not registered
- Show info message that report was successful
- Handle adding new esx host
- Fail before forking when password key does not exist
- Filter out all host when filter_host_uuids is empty
- Resolves: rhbz#1212334

* Thu Apr 09 2015 Radek Novacek <rnovacek@redhat.com> 0.12-5
- Properly handle reload requests
- Don't check pidfile when running --help
- Resolves: rhbz#1208391, rhbz#1210209

* Tue Apr 07 2015 Radek Novacek <rnovacek@redhat.com> 0.12-4
- ESX: support esx update sets that are splitted to several parts
- Resolves: rhbz#1155679

* Thu Apr 02 2015 Radek Novacek <rnovacek@redhat.com> 0.12-3
- ESX: Relogin after connection failure
- Don't fail when encryption key doesn't exist
- Fix reloading and termination of processes
- Resolves: rhbz#1208345, rhbz#1208029, rbhz#1208020, rhbz#1207971, rhbz#1208391

* Tue Mar 24 2015 Radek Novacek <rnovacek@redhat.com> 0.12-2
- Fix proxy support in ESX
- Fix timeout error in ESX
- Update options for Satellite naming
- Allow to identify hypervisors by other properties than UUID
- Related: rhbz#1195585
- Resolves: rbhz#1197970

* Fri Feb 27 2015 Radek Novacek <rnovacek@redhat.com> 0.12-1
- Rebase to virt-who-0.12
- Resolves: rhbz#1195585

* Wed Sep 10 2014 Radek Novacek <rnovacek@redhat.com> 0.10-8
- Fix domain sorting error in vdsm mode
- Resolves: rhbz#1139497

* Fri Aug 29 2014 Radek Novacek <rnovacek@redhat.com> 0.10-7
- vdsm and rhevm: fix constructor parameters
- Resolves: rhbz#1135341

* Fri Aug 08 2014 Radek Novacek <rnovacek@redhat.com> 0.10-6
- esx: disable error when esx host doesn't have guests
- hyperv: don't use deprecated md5 module
- Resolves: rhbz#1126295, rhbz#1126302

* Fri Aug 01 2014 Radek Novacek <rnovacek@redhat.com> 0.10-5
- libvirt: properly handle libvirt shutdown when doing background monitoring
- Resolves: rhbz#1125810

* Tue Jul 29 2014 Radek Novacek <rnovacek@redhat.com> 0.10-4
- Fix wrong usage of hypervisorCheckIn function
- Fix wrong logger usage when processing update errors
- Resolves: rhbz#1123723

* Wed Jul 02 2014 Radek Novacek <rnovacek@redhat.com> 0.10-3
- libvirtd: use event loop instead of reconnecting all the time
- Resolves: rhbz#1113938

* Wed Jun 18 2014 Radek Novacek <rnovacek@redhat.com> 0.10-2
- Add upstream fixes of 0.10 release
- Related: rhbz#1002640

* Tue Jun 03 2014 Radek Novacek <rnovacek@redhat.com> 0.10-1
- Rebase to virt-who-0.10
- Resolves: rhbz#1002640

* Thu Aug 29 2013 Radek Novacek <rnovacek@redhat.com> 0.8-9
- Set SAM mode as default
- Fix esx traversal patch
- Resolves: rhbz#1002058, rhbz#996269

* Thu Aug 22 2013 Radek Novacek <rnovacek@redhat.com> 0.8-8
- Add satellite support
- Handle more than 100 objects in esx traversal
- Resolves: rhbz#1002058, rhbz#996269

* Wed Aug 07 2013 Radek Novacek <rnovacek@redhat.com> 0.8-7
- Use instanceUuid when uuid of virtual machine is empty
- Resolves: rhbz#923757

* Fri Jul 26 2013 Radek Novacek <rnovacek@redhat.com> 0.8-6
- Increase compatibility with ESXi
- Resolves: rhbz#923757

* Thu Oct 25 2012 Radek Novacek <rnovacek@redhat.com> 0.8-5
- Fix adding https:// to ESX url
- Resolves: rhbz#869960

* Wed Oct 24 2012 Radek Novacek <rnovacek@redhat.com> 0.8-4
- Help and manpage improvements
- Resolves: rhbz#868149

* Wed Oct 17 2012 Radek Novacek <rnovacek@redhat.com> 0.8-3
- Fix bugs in Hyper-V support (patch rebased)
- Create PID file ASAP to prevent service stop fails
- Resolves: rhbz#866890

* Thu Oct 11 2012 Radek Novacek <rnovacek@redhat.com> 0.8-2
- Add support for accessing Hyper-V
- Resolves: rhbz#860854

* Wed Sep 26 2012 Radek Novacek <rnovacek@redhat.com> 0.8-1
- Upstream version 0.8
- RFE: command line improvements
- Add support for accessing RHEV-M
- Fix printing tracebacks on terminal
- Resolves: rhbz#808060, rhbz#846788, rhbz#825215

* Thu Apr 26 2012 Radek Novacek <rnovacek@redhat.com> 0.6-6
- Handle unknown libvirt event properly
- Resolves: rhbz#815279

* Wed Apr 18 2012 Radek Novacek <rnovacek@redhat.com> 0.6-5
- Enable debug output to be written to stderr
- Log guest list to log even in non-debug mode
- Resolves: rhbz#813299

* Tue Apr 17 2012 Radek Novacek <rnovacek@redhat.com> 0.6-4
- Fix regression in double fork patch
- Resolves: rhbz#813299

* Wed Mar 28 2012 Radek Novacek <rnovacek@redhat.com> 0.6-3
- Do double fork when daemon is starting
- Resolves: rhbz#806225

* Fri Mar 09 2012 Radek Novacek <rnovacek@redhat.com> 0.6-2
- Add python-suds require
- Requires python-rhsm >= 0.98.6
- Resolves: rhbz#801657

* Thu Mar 01 2012 Radek Novacek <rnovacek@redhat.com> 0.6-1
- Rebase to virt-who-0.6
- Resolves: rhbz#790000

* Wed Oct 12 2011 Radek Novacek <rnovacek@redhat.com> 0.3-3
- Use updateConsumer API instead of updateConsumerFact (fixes limit 255 chars of uuid list)
- Requires python-rhsm >= 0.96.13 
- Resolves: rhbz#743823

* Wed Sep 07 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-2
- Add upstream patch that prevents failure when server not implements /status/ command
- Resolves: rhbz#735793

* Thu Sep 01 2011 Radek Novacek <rnovacek@redhat.com> - 0.3-1
- Add initscript and configuration file

* Mon Aug 22 2011 Radek Novacek <rnovacek@redhat.com> - 0.2-2
- Bump release because of tagging in wrong branch

* Mon Aug 22 2011 Radek Novacek <rnovacek@redhat.com> - 0.2-1
- Update to upstream version 0.2
- Add Requires: libvirt

* Fri Aug 19 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-2
- Add BuildRoot tag (the package will be in RHEL5)

* Wed Aug 10 2011 Radek Novacek <rnovacek@redhat.com> - 0.1-1
- initial import
