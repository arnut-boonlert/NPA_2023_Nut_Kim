from netmiko import ConnectHandler

def send_command(device_params, commands):
    with ConnectHandler(**device_params) as ssh:
        for command in commands:
            ssh.send_command(command, expect_string=r"\S+#")


def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command(command)
    return result

def get_ip(device_params, intf):
    command = 'sh ip int br'
    result = get_data_from_device(device_params, command) 
    for lines in result.strip().split('\n'): #Ex: GigabitEthernet0/0    172.31.108.4
        line = lines.split() #Ex: ['GigabitEthernet0/0', '172.31.108.4']
        if intf in line[0][0] + line[0][-3:]: #Ex: line[0][0]='G' and line[0][-3:]='0/0'
            ip_add = line[1] #get ip which matched intf
            return ip_add

def get_cdp_nei(device_params, intf):
    command = 'show cdp nei'
    result = get_data_from_device(device_params, command)
    lines = result.strip().split('\n')
    header_index = lines.index('Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID')
    ender_index = lines.index('', lines.index('')+1) #the second one of blank line in result
    for i in range (header_index+1, ender_index): #start from next line of header_index and stop at ender_index
        local_intf = lines[i].split()[1][0] + lines[i].split()[2] #Ex: 'Gig 0/0' -> 'G0/0'
        if intf == local_intf:
            device_id = lines[i].split('.')[0] #get device id Ex: S0 (from 'S0.npa.com') 
            port_id = lines[i].split()[-2][0] + lines[i].split()[-1] #get port id Ex: 'Gig 0/2' -> 'G0/2'
            return f'Connect to {port_id} of {device_id}'
        elif i == ender_index-1: #if nothing matched
            return 'Not Use'

def set_desc(device_params, intf):
    commands = ['conf t', f'int {intf}', f'des {get_cdp_nei(device_params, intf)}', 'end']
    send_command(device_params, commands)

def get_only_desc(device_params, intf):
    command = 'show int des'
    result = get_data_from_device(device_params, command)
    lines = result.strip().split('\n')
    lines.pop(0)
    return lines

def get_desc(device_params, intf, skip_get_desc='True'):#let it True because int des has configured
    if not skip_get_desc:
        set_desc(device_params, intf)
    lines = get_only_desc(device_params, intf)
    for line in lines:
        local_intf = line.split()[0][0] + line.split()[0][-3:] #get local_intf Ex: G0/0
        if intf == local_intf:
            line = line.split()
            check_status = line[1] == 'up' and line[2] == 'up' #check status and protocol status
            if check_status: #if status and protocol is up up
                words = line.index('Connect') #find 'Connect' in list
            else:
                words = line.index('Not') #find 'Not' in list
            word = ''
            for i in range (words, len(line)): #start with index of words 
                word = f'{word} {line[i]}' 
                word = word.strip() #the result is description Ex: Connect to G0/2 of S0
    return word


def get_status(device_params, intf):
    lines = get_only_desc(device_params, intf)
    for line in lines:
        local_intf = line.split()[0][0] + line.split()[0][-3:] #get local_intf Ex: G0/0
        line = line.split()
        if intf == local_intf:
            check_status = line[1] == 'up' and line[2] == 'up' #check status and protocol status
            if check_status:#if status and protocol is up up
                status = f'{line[1]} {line[2]}' #Ex: up up
            else:
                status = f'{line[1]} {line[2]} {line[3]}'#Ex: admin down down
    return status

if __name__ == '__main__':
    devices_ip = ['172.31.108.4', '172.31.108.5', '172.31.108.6']
    username = 'admin'
    password = 'cisco'
    devices_params = []
    for i in range(len(devices_ip)):
        device_params = {'device_type': 'cisco_ios', 
        'ip': devices_ip[i], 
        'username': username, 
        'password': password, 
        'global_delay_factor': 0.1}
        devices_params.append(device_params)

