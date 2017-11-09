from distutils import spawn

import os
import re
import subprocess
import time
import unittest

import qubes.tests
import qubes.qubes

from qubes.qubes import QubesVmCollection

class SD_VM_Tests(unittest.TestCase):
  def setUp(self):
    self.qc = QubesVmCollection()
    self.qc.lock_db_for_reading()
    self.qc.load()

  def tearDown(self):
    self.qc.unlock_db()

  def test_expected(self):
    vms = [v.name for v in self.qc.values()]
    vm_set = set(vms)

    for test_vm in ["sd-whonix", "sd-journalist", "sd-svs", "fedora-25-sd-dispvm"]:
      self.assertTrue(test_vm in vm_set)

  def test_sd_whonix_net(self):
    vm = self.qc.get_vm_by_name("sd-whonix")
    nvm = vm.netvm
    self.assertTrue(nvm.name == "sys-firewall")

  def test_sd_journalist_net(self):
    vm = self.qc.get_vm_by_name("sd-journalist")
    nvm = vm.netvm
    self.assertTrue(nvm.name == "sd-whonix")

  def test_sd_svs_net(self):
    vm = self.qc.get_vm_by_name("sd-svs")
    nvm = vm.netvm
    self.assertTrue(nvm is None)

  def test_sd_dispvm_net(self):
    vm = self.qc.get_vm_by_name("fedora-25-sd-dispvm")
    nvm = vm.netvm
    self.assertTrue(nvm.name == "sys-firewall")

def load_tests(loader, tests, pattern):
  suite = unittest.TestLoader().loadTestsFromTestCase(SD_VM_Tests)
  return suite
