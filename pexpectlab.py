import pexpect

PROMPT = '#'
USERNAME = 'admin'
PASSWORD = 'cisco'

def loopback():
    devices_ip = ['172.31.108.4', '172.31.108.5', '172.31.108.6']
    for ip in devices_ip:
        child = pexpect.spawn('telnet ' + ip)
        child.expect('Username')
        child.sendline(USERNAME)
        child.expect('Password')
        child.sendline(PASSWORD)
        num = str(devices_ip.index(ip)+1)
        loopback_ip = f"ip add {num}.{num}.{num}.{num} 255.255.255.255"
        commands = ['conf t' ,'int lo 0', loopback_ip, 'end']
        for command in commands:
            child.expect(PROMPT)
            child.sendline(command)
        child.expect(PROMPT)
        child.sendline('show ip int br')
        child.expect(PROMPT)
        child.sendline('exit')
        result = child.before
        print(result.decode('UTF-8'))
        print()
        
loopback()
