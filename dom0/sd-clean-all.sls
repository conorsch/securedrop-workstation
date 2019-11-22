# -*- coding: utf-8 -*-
# vim: set syntax=yaml ts=2 sw=2 sts=2 et :

set-fedora-as-default-dispvm:
  cmd.run:
    - name: qubes-prefs default_dispvm fedora-30-dvm

remove-dom0-sdw-config-files:
  file.absent:
    - names:
      - /opt/securedrop
      - /etc/yum.repos.d/securedrop-workstation-dom0.repo
      - /usr/bin/securedrop-update
      - /etc/pki/rpm-gpg/RPM-GPG-KEY-securedrop-workstation-test
      - /etc/cron.daily/securedrop-update-cron
      - /usr/share/securedrop/icons

{% set sdw_vms = salt['cmd.run']('qvm-ls --tags sd-workstation --raw-list').splitlines() %}
{% for sdw_vm in sdw_vms %}

halt-sdw-vm-{{ sdw_vm }}:
  qvm.kill:
    - name: {{ sdw_vm }}
    - onlyif:
      - qvm-check --running {{ sdw_vm }}

remove-sdw-vm-appvms-{{ sdw_vm }}:
  qvm.absent:
    - name: {{ sdw_vm }}
    - require:
      - cmd: set-fedora-as-default-dispvm
      - qvm: halt-sdw-vm-{{ sdw_vm }}
    - unless:
      - qvm-check --template {{ sdw_vm }}

remove-sdw-vm-templates-{{ sdw_vm }}:
  qvm.absent:
    - name: {{ sdw_vm }}
    - require:
      - qvm: remove-sdw-vm-appvms-{{ sdw_vm }}
    - order: last
    - onlyif:
      - qvm-check --template {{ sdw_vm }}
      - bash -c 'test $(qvm-prefs {{ sdw_vm }} installed_by_rpm) == False'

{% endfor %}

sd-cleanup-sys-firewall:
  cmd.run:
    - names:
      - qvm-run sys-firewall 'sudo rm -f /rw/config/RPM-GPG-KEY-securedrop-workstation-test'
      - qvm-run sys-firewall 'sudo rm -f /rw/config/sd-copy-rpm-repo-pubkey.sh'
      - qvm-run sys-firewall 'sudo rm -f /etc/pki/rpm-gpg/RPM-GPG-KEY-securedrop-workstation-test'
      - qvm-run sys-firewall 'sudo perl -pi -E "s#^/rw/config/sd-copy-rpm-repo-pubkey.sh##" /rw/config/rc.local'

{% for rpc_file in ['qubes.VMShell', 'qubes.VMRootShell'] %}
sd-cleanup-rpc-mgmt-policy-{{ rpc_file }}:
  file.line:
    - name: /etc/qubes-rpc/policy/{{ rpc_file }}
    - mode: delete
    - match: '^disp-mgmt-sd-\w+\s+sd-\w+\s+allow,user=root'
    - only-if:
      - grep -qP '^disp-mgmt-sd-' /etc/qubes-rpc/policy/{{ rpc_file }}
{% endfor %}
