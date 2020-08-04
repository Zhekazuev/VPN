"""
Methods need to work with CORPs(Ultra)
"""
from config import Corps
import paramiko
import time


class SSH:
    def __init__(self, host, user, password, port=22):
        self.client = None
        self.conn = None
        self.host = host
        self.user = user
        self.password = password
        self.port = port

    def connect(self):
        """Open ssh connection."""
        if self.conn is None:
            try:
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(hostname=self.host, port=self.port, username=self.user, password=self.password)
                return self.client
            except paramiko.AuthenticationException as authException:
                print(f"{authException}, please verify your credentials")
            except paramiko.SSHException as sshException:
                print(f"Could not establish SSH connection: {sshException}")

    def shell(self, cmd, pause=5):
        """"""
        with self.connect().invoke_shell() as shell:
            shell.send(cmd)
            time.sleep(pause)
            output = shell.recv(10000).decode('utf8')
            return output

    def execute_commands(self, cmd):
        """
        Execute command in succession.

        :param cmd: One command for example: show administrators
        :type cmd: str
        """
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdout.channel.recv_exit_status()
        response = stdout.readlines()
        return response

    def put(self, localpath, remotepath):
        sftp = self.client.open_sftp()
        sftp.put(localpath, remotepath)
        time.sleep(10)
        sftp.close()
        self.client.close()

    def get(self, remotepath, localpath):
        sftp = self.client.open_sftp()
        sftp.get(remotepath, localpath)
        time.sleep(10)
        sftp.close()
        self.client.close()

    def disconnect(self):
        """Close ssh connection."""
        if self.client:
            self.client.close()


class VRF:
    def __init__(self, context="Gi-3", vrf_name="", pool_name="", ip_pool="", mask_pool="",
                 router_bgp=64633, loopback="", rd=10000, remote_as=25106):
        self.context = context
        self.vrf_name = vrf_name
        self.pool_name = pool_name
        self.ip_pool = ip_pool
        self.mask_pool = mask_pool
        self.router_bgp = router_bgp
        self.loopback = loopback
        self.rd = rd
        self.remote_as = remote_as

    def create(self):
        """
        Make a executing create command
        :return: Command to create one vrf. Use this command for execute.
        """
        command = f"config\n" \
                  f"context {self.context}\n" \
                  f"ip vrf {self.vrf_name}\n" \
                  f"router bgp {self.router_bgp}\n" \
                  f"ip vrf {self.vrf_name}\n" \
                  f"route-distinguisher {self.loopback} {self.rd}\n" \
                  f"route-target both {self.remote_as} {self.rd}\n" \
                  f"exit\n" \
                  f"address-family ipv4 vrf {self.vrf_name}\n" \
                  f"redistribute connected route-map set_BGP_community\n" \
                  f"end\n"
        return command

    def update(self):
        pass

    def delete(self):
        """
        Make a executing delete command
        :return: Command to delete one vrf. Use this command for execute.
        """
        command = f"config\n" \
                  f"context {self.context}\n" \
                  f"no ip vrf {self.vrf_name}\n" \
                  f"end\n"
        return command


class Pool:
    def __init__(self, context="Gi-3", vrf_name="", pool_name="", ip_pool="", mask_pool="", group_name=""):
        """
        Init parameters for work with pools
        :param context: Gi-3
        :param vrf_name: 10000_test
        :param pool_name: 10000_test_1
        :param ip_pool: 10.10.145.224
        :param mask_pool: 255.255.255.240
        :param group_name: 10000_test
        """
        self.context = context
        self.vrf_name = vrf_name
        self.group_name = group_name
        self.pool_name = pool_name
        self.ip_pool = ip_pool
        self.mask_pool = mask_pool

    def create(self):
        """
        Make a executing create command
        :return: Command to create one pool. Use this command for execute
        """
        command = f"config\n" \
                  f"context {self.context}\n" \
                  f"ip vrf {self.vrf_name}\n" \
                  f"ip pool {self.pool_name} {self.ip_pool} {self.mask_pool} " \
                  f"static srp-activate group-name {self.group_name} vrf {self.vrf_name}\n" \
                  f"end\n"
        return command

    def update(self):
        """
        Make a executing update command
        :return: Command to update one pool. Use this command for execute
        """
        command = f"config\n" \
                  f"context {self.context}\n" \
                  f"ip vrf {self.vrf_name}\n" \
                  f"no ip pool {self.pool_name} {self.ip_pool} {self.mask_pool} " \
                  f"static srp-activate group-name {self.group_name} vrf {self.vrf_name}\n" \
                  f"ip pool {self.pool_name} {self.ip_pool} {self.mask_pool} " \
                  f"static srp-activate group-name {self.group_name} vrf {self.vrf_name}\n" \
                  f"end\n"
        return command

    def delete(self):
        """
        Make a executing delete command
        :return: Command to delete one pool. Use this command for execute.
        """
        command = f"config\n" \
                  f"context {self.context}\n" \
                  f"ip vrf {self.vrf_name}\n" \
                  f"no ip pool {self.pool_name}\n" \
                  f"end\n"
        return command


if __name__ == '__main__':
    pass
    # ip_corp_1 = Corps.IP_CORP_1
    # ip_corp_2 = Corps.IP_CORP_2
    # user = Corps.STAROS_SCRIPTS_TACACS_USER
    # password = user = Corps.STAROS_SCRIPTS_TACACS_PASS
    # ssh = SSH(host=Corps.IP_TEST_ASR, user=Corps.STAROS_TEST_ASR_USER, password=Corps.STAROS_TEST_ASR_PASS)
    # connect = ssh.connect()
    # cmd = 'config\n' \
    #       'context Gi-3\n' \
    #       'ip vrf 10305_ugk\n' \
    #       'ip pool 10305_ugk_1 10.10.145.224 255.255.255.240 ' \
    #       'static srp-activate group-name 10305_ugk vrf 10305_ugk\n' \
    #       'ip pool 10305_ugk_2 10.10.147.64 255.255.255.224 ' \
    #       'static srp-activate group-name 10305_ugk vrf 10305_ugk\n' \
    #       'router bgp 64633\n' \
    #       'ip vrf 10305_ugk\n' \
    #       'route-distinguisher 172.24.249.4 10305\n' \
    #       'route-target both 25106 10305\n' \
    #       'exit\n' \
    #       'address-family ipv4 vrf 10305_ugk\n' \
    #       'redistribute connected route-map set_BGP_community\n' \
    #       'end\n'
    # create client(vrf + pool)
    # ssh.shell(cmd, pause=2)
    # print(ssh.shell('show configuration context Gi-3 | grep 10305\n', pause=5))

    # create vrf
    # vrf_create = VRF(context="Gi-3", vrf_name="10307_test", router_bgp=64633,
    #                  loopback="172.24.249.4", rd=10307, remote_as=25106).create()
    # ssh.shell(vrf_create)
    # print(ssh.shell('show configuration context Gi-3 | grep 10307\n', pause=5))

    # create pool
    # pool_create = Pool(context="Gi-3", vrf_name="10307_test", pool_name="10307_test_1",
    #                    ip_pool="10.10.145.224", mask_pool="255.255.255.240",
    #                    group_name="10307_test").create()
    # ssh.shell(pool_create)
    # print(ssh.shell('show configuration context Gi-3 | grep 10307\n', pause=5))

    # delete client(vrf + pool)
    # vrf_del = VRF(context="Gi-3", vrf_name="10307_test").delete()
    # ssh.shell(vrf_del)
    # print(ssh.shell('show configuration context Gi-3 | grep 10307\n', pause=5))

    # delete pool
    # pool_del = Pool(context="Gi-3", vrf_name="10307_test", pool_name="10307_test_1").delete()
    # ssh.shell(pool_del)
    # print(ssh.shell('show configuration context Gi-3 | grep 10307\n', pause=5))
    # ssh.disconnect()
