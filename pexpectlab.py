import pexpect

PROMPT = '#'
IP = '10.0.14.112'
USERNAME = 'admin'
PASSWORD = 'cisco'
COMMAND = 'sh ip int br'

devices_ip = ["172.31.108.4", "172.31.108.5", "172.31.108.6"]

for ip in devices_ip:
    child = pexpect.spawn('telnet ' + IP)
    child.expect('Username')
    child.sendline(USERNAME)
    child.expect('Password')
    child.sendline(PASSWORD)
    child.expect(PROMPT)
    child.sendline(COMMAND)
    child.expect(PROMPT)
    result = child.before
    print(result)
    print()
    print(result.decode('UTF-8'))
    child.sendline('exit')
    print("test")