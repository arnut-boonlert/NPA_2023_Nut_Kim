import pexpect

PROMPT = '#'
IP = '172.31.108.4'
USERNAME = 'admin'
PASSWORD = 'cisco'
COMMAND = 'sh ip int br'

devices_ip = ["172.31.108.4", "172.31.108.5", "172.31.108.6"]
child = pexpect.spawn('telnet ' + IP)
child.expect('Username')
child.sendline(USERNAME)
child.expect('Password')
child.sendline(PASSWORD)
child.expect(PROMPT)
child.sendline(COMMAND)
child.expect(PROMPT)
result = child.before
print(result.decode('UTF-8'))
child.sendline('exit')