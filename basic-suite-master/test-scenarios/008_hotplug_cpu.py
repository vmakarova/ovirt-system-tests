import nose.tools as nt
import os

from ovirtsdk.xml import params
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
    
    open('known_hosts', 'w').close()
    client = ssh.get_ssh_client(
        ip_addr='192.168.201.213',
        ssh_key='known_hosts', 
        username='cirros',
        password='cubswin:)'
    )
    command = 'lscpu | grep CPU\'(\'s\')\':'
    stdin, out, err = client.exec_command(command)
    cpu_number = out.read().splitlines()[0].split(":")[1].strip()
    client.close()
    os.remove('known_hosts')
    nt.assert_true(int(cpu_number) == 2)



_TEST_LIST = [
    hotplug_cpu,
]


def test_gen():
    for t in testlib.test_sequence_gen(_TEST_LIST):
        test_gen.__name__ = t.description
        yield t
