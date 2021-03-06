Name:		securedrop-workstation-dom0-config
Version:	0.1.1
Release:	1%{?dist}
Summary:	SecureDrop Workstation

Group:		Library
License:	GPLv3+
URL:		https://github.com/freedomofpress/securedrop-workstation
Source0:	securedrop-workstation-dom0-config-0.1.1.tar.gz

BuildArch:      noarch
BuildRequires:	python3-setuptools
BuildRequires:	python3-devel

# This package installs all standard VMs in Qubes
Requires:       qubes-mgmt-salt-dom0-virtual-machines

%description

This package contains VM configuration files for the Qubes-based
SecureDrop Workstation project. The package should be installed
in dom0, or AdminVM, context, in order to manage updates to the VM
configuration over time.

%prep
%setup -q


%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --skip-build --root %{buildroot}
install -m 755 -d %{buildroot}/opt/securedrop/launcher
install -m 755 -d %{buildroot}/opt/securedrop/launcher/sdw_updater_gui
install -m 755 -d %{buildroot}/srv
install -m 755 -d %{buildroot}/srv/salt/sd
install -m 755 -d %{buildroot}/srv/salt/sd/sd-app
install -m 755 -d %{buildroot}/srv/salt/sd/sd-proxy
install -m 755 -d %{buildroot}/srv/salt/sd/sd-journalist
install -m 755 -d %{buildroot}/srv/salt/sd/sd-whonix
install -m 755 -d %{buildroot}/srv/salt/sd/sd-workstation
install -m 755 -d %{buildroot}/srv/salt/sd/sys-firewall
install -m 755 -d %{buildroot}/usr/share/%{name}/scripts
install -m 755 -d %{buildroot}/srv/salt/sd/usb-autoattach
install -m 644 dom0/*.sls %{buildroot}/srv/salt/
install -m 644 dom0/*.top %{buildroot}/srv/salt/
install -m 644 dom0/*.j2 %{buildroot}/srv/salt/
install -m 644 dom0/securedrop-update %{buildroot}/srv/salt/
install -m 644 dom0/securedrop-login %{buildroot}/srv/salt/
install -m 644 dom0/securedrop-launcher.desktop %{buildroot}/srv/salt/
install -m 655 dom0/securedrop-handle-upgrade %{buildroot}/srv/salt/
# The next file should get installed via RPM not via salt
install -m 755 dom0/securedrop-update %{buildroot}/srv/salt/securedrop-update
install -m 644 sd-app/* %{buildroot}/srv/salt/sd/sd-app/
install -m 644 sd-proxy/* %{buildroot}/srv/salt/sd/sd-proxy/
install -m 644 sd-whonix/* %{buildroot}/srv/salt/sd/sd-whonix/
install -m 644 sd-workstation/* %{buildroot}/srv/salt/sd/sd-workstation/
install -m 644 sys-firewall/* %{buildroot}/srv/salt/sd/sys-firewall/
install -m 644 usb-autoattach/99-sd-devices.rules %{buildroot}/srv/salt/sd/usb-autoattach/
install -m 755 usb-autoattach/sd-attach-export-device %{buildroot}/srv/salt/sd/usb-autoattach/
install -m 644 Makefile %{buildroot}/usr/share/%{name}/Makefile
install -m 755 scripts/* %{buildroot}/usr/share/%{name}/scripts/
install -m 644 launcher/*.py %{buildroot}/opt/securedrop/launcher/
install -m 644 launcher/sdw_updater_gui/*.py %{buildroot}/opt/securedrop/launcher/sdw_updater_gui/
%files
%doc README.md LICENSE
%{python3_sitelib}/securedrop_workstation_dom0_config*
%{_datadir}/%{name}
%{_bindir}/securedrop-update
/srv/salt/sd*
/srv/salt/dom0-xfce-desktop-file.j2
/srv/salt/securedrop-*
/srv/salt/fpf*
/opt/securedrop/*

%post
find /srv/salt -maxdepth 1 -type f -iname '*.top' \
    | xargs -n1 basename \
    | sed -e 's/\.top$$//g' \
    | xargs qubesctl top.enable > /dev/null

%changelog
* Fri Jan 10 2020 redshiftzero <jen@freedom.press> - 0.1.1
- First alpha release.

* Fri Oct 26 2018 Kushal Das <kushal@freedom.press> - 0.0.1-1
- First release
