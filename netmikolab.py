from netmiko import ConnectHandler

def send_command(ssh, commands):
    for command in commands:
        result = ssh.send_command(command, expect_string=r"\S+#")


def get_data_from_device(ssh, command):
    result = ssh.send_command(command)
    return result

def get_ip(device_params, intf):
    with ConnectHandler(**device_params) as ssh:
        command = 'sh ip int br'
        result = get_data_from_device(ssh, command) 
        for lines in result.strip().split('\n'): #Ex: GigabitEthernet0/0    172.31.108.4
            line = lines.split() #Ex: ['GigabitEthernet0/0', '172.31.108.4']
            if intf in line[0][0] + line[0][-3:]: #Ex: line[0][0]='G' and line[0][-3:]='0/0'
                ip_add = line[1] #get ip which matched intf
                return ip_add

def get_cdp_nei(device_params, intf):
    with ConnectHandler(**device_params) as ssh:
        command = 'show cdp nei'
        result = get_data_from_device(ssh, command)
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

def get_desc(device_params, intf):
     with ConnectHandler(**device_params) as ssh:
        commands = ['conf t', f'int {intf}', f'des {get_cdp_nei(device_params, intf)}', 'end']
        send_command(ssh, commands)
        command = 'show int des'
        result = get_data_from_device(ssh, command)
        lines = result.strip().split('\n')
        lines.pop(0)
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
                    word = word.strip()
        return word

        if intf == 'G0/0':
            commands = ['conf t', 'int g0/0', 'des Connect to G0/2 of S0', 'end']
            send_command(ssh, commands)
            command = 'show int des'
            result = get_data_from_device(ssh, command)
            lines = result.strip().split('\n')
            line = lines[1].split()

        elif intf == 'G0/1':
            commands = ['conf t', 'int g0/1', 'des Connect to G0/2 of S1', 'end']
            send_command(ssh, commands)
            command = 'show int des'
            result = get_data_from_device(ssh, command)
            lines = result.strip().split('\n')
            line = lines[2].split()
        words = line.index('Connect')
        word = ''
        for i in range (words, len(line)):
            word = f'{word} {line[i]}'
        word = word.strip()
        return word
        

        
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
    # print(get_desc(devices_params[0], 'G0/0'))
    print(get_desc(devices_params[0], 'G0/3'))

            # print(get_ip(devices_params[i], 'G0/1'))
            # print(get_ip(devices_params[i], 'G0/2'))
            # print(get_ip(devices_params[i], 'G0/3'))




# def get_mask(device_params, intf):
#     command = 'show ip route vrf management | include ^C'
#     data = get_data_from_device(device_params, command) #C 72.31.108.0/28 is directly connected, GigabitEthernet0/0
#     intf_name = data.split(',')[-1] # example output: GigabitEthernet0/0
#     intf_name = (intf_name[1] + intf_name[-3:]) #get first and last 3 lettes example output: G0/0
#     if intf == intf_name:
#         index = data.find('/')
#         result = '/' + data[index+1:index+3]
#         return result
#     return ''




# data = """Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
    #       S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
    #       D - Remote, C - CVTA, M - Two-port Mac Relay

    #       Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
    #       S1.npa.com       Gig 0/1           133              S I             Gig 0/2
    #       S0.npa.com       Gig 0/0           135              S I             Gig 0/2
    #       R2.npa.com       Gig 0/2           177              R B             Gig 0/1"""

    # local_intf = interface_line.split()[1][0] + interface_line.split()[2]


def get_mask(device_params, intf):
    command = 'show ip route vrf management | include ^C'
    data = get_data_from_device(device_params, command) #example output: C 72.31.108.0/28 is directly connected, GigabitEthernet0/0
    index = data.find('/') #find index for '/'
    result = '/' + data[index+1:index+3] #/28
    return result





def get_status(device_params, intf):
    valid_intfs = ['G0/0', 'G0/1', 'G0/2']
    if intf in valid_intfs:
        return 'up/up'
    else:
        return 'administratively down/down'
