import nose.tools as nt
import paramiko

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
    
    host = '192.168.201.213'
    user = 'cirros'
    secret = 'cubswin:)'
    port = 22
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('lscpu | grep CPU\'(\'s\')\':')
    cpu_number = stdout.read().splitlines()[0].split(":")[1].strip()
    client.close()
    nt.assert_true(int(cpu_number) == 2)



_TEST_LIST = [
    hotplug_cpu,
]


def test_gen():
    for t in testlib.test_sequence_gen(_TEST_LIST):
        test_gen.__name__ = t.description
        yield t
