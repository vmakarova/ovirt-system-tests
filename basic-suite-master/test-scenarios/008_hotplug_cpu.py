import functools
import os
import nose.tools as nt
from nose import SkipTest

from ovirtsdk.xml import params
import ovirtsdk.api
from ovirtsdk.infrastructure.brokers import VMs
from lago import utils
from ovirtlago import testlib


VM0_NAME = 'vm0'


@testlib.with_ovirt_api
def hotplug_cpu(api):
    topology = params.CpuTopology(
        cores=1,
        threads=1,
        sockets=2,
    )
    vm = api.vms.get(VM0_NAME)
    vm.cpu.topology = topology
    nt.assert_true(
        vm.update()
    )
    nt.assert_true(api.vms.get(VM0_NAME).cpu.topology.sockets == 2)


_TEST_LIST = [
    hotplug_cpu,
]


def test_gen():
    for t in testlib.test_sequence_gen(_TEST_LIST):
        test_gen.__name__ = t.description
        yield t