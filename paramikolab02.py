import time
import paramiko
import getpass

USERNAME = 'LINUX_USER'
devices_ip = ["172.31.108.4", "172.31.108.5", "172.31.108.6"]
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
private_key = paramiko.RSAKey.from_private_key_file("/home/devasc/.ssh/id_rsa")

def send_command(ssh, command):
    ssh.send(command + '\n')
    time.sleep(1)
    result = ssh.recv(1000).decode('ascii')
    print(result)

def configure_r1(ip):
    client.connect(hostname=ip, username=USERNAME, pkey=private_key)
    print('Connecting to {} ...'.format(ip))
    with client.invoke_shell() as ssh:
        print('connected to {} ...'.format(ip))
        send_command(ssh, 'terminal length 0')
        send_command(ssh, 'en')
        send_command(ssh, password)
        send_command(ssh, 'conf t')
        send_command(ssh, 'router ospf 1 vrf control-data')
        send_command(ssh, 'network 172.31.108.16 0.0.0.15 area 0')
        send_command(ssh, 'network 172.31.108.32 0.0.0.15 area 0')
        send_command(ssh, 'network 1.1.1.1 0.0.0.0 area 0')

def configure_r2(ip):
    client.connect(hostname=ip, username=USERNAME, pkey=private_key)
    print('Connecting to {} ...'.format(ip))
    with client.invoke_shell() as ssh:
        print('connected to {} ...'.format(ip))
        send_command(ssh, 'terminal length 0')
        send_command(ssh, 'en')
        send_command(ssh, password)
        send_command(ssh, 'conf t')
        send_command(ssh, 'router ospf 1 vrf control-data')
        send_command(ssh, 'network 172.31.108.32 0.0.0.15 area 0')
        send_command(ssh, 'network 172.31.108.48 0.0.0.15 area 0')
        send_command(ssh, 'network 2.2.2.2 0.0.0.0 area 0')

def configure_r3(ip):
    client.connect(hostname=ip, username=USERNAME, pkey=private_key)
    print('Connecting to {} ...'.format(ip))
    with client.invoke_shell() as ssh:
        print('connected to {} ...'.format(ip))
        send_command(ssh, 'terminal length 0')
        send_command(ssh, 'en')
        send_command(ssh, password)
        send_command(ssh, 'conf t')
        send_command(ssh, 'router ospf 1 vrf control-data')
        send_command(ssh, 'network 172.31.108.48 0.0.0.15 area 0')
        send_command(ssh, 'network 3.3.3.3 0.0.0.0 area 0')
        send_command(ssh, 'default-information originate')
        send_command(ssh, 'int g0/2')
        send_command(ssh, 'no sh')
        send_command(ssh, 'vrf forwarding control-data')
        send_command(ssh, 'ip add dhcp')
        send_command(ssh, 'ip nat outside')
        send_command(ssh, 'int g0/1')
        send_command(ssh, 'ip nat inside')
        send_command(ssh, 'exit')
        for ip_add in devices_ip:
            # send_command(ssh, 'access-list 1 permit tcp host 172.31.108.0 0.0.0.15 host {} eq telnet'.format(ip_add))
            # send_command(ssh, 'access-list 1 permit tcp host 172.31.108.0 0.0.0.15 host {} eq ssh'.format(ip_add))
            send_command(ssh, 'access-list 100 deny tcp any host {} eq telnet'.format(ip_add))
            send_command(ssh, 'access-list 100 deny tcp any host {} eq 22'.format(ip_add))
        send_command(ssh, 'access-list 100 permit ip any any')
        send_command(ssh, 'access-list 100 permit ip any any')
        # send_command(ssh, 'access-list 1 permit any')
        send_command(ssh, 'ip nat inside source list 100 interface g0/2 overload')
        
#password = getpass.getpass()
password = 'hello'
# configure_r1(devices_ip[0])
# configure_r2(devices_ip[1])
configure_r3(devices_ip[2])