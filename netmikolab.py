from netmiko import ConnectHandler
import paramiko


def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command(command)
        return result


def get_ip(device_params, intf):
    command = 'sh ip int br'
    data = get_data_from_device(device_params, command)
    result = data.strip().split('\n')
    for line in result[1:]:
        words = line.split()
        if words[0][0] == intf[0] and words[0][-3:] == intf[1:]:
            return words[1]

def get_mask(device_params, intf):
    command = 'show ip route vrf management | include ^C'
    data = get_data_from_device(device_params, command) #example output: C 72.31.108.0/28 is directly connected, GigabitEthernet0/0
    index = data.find('/') #find index for '/'
    result = '/' + data[index+1:index+3] #/28
    return result

def get_desc(device_params, intf):
    command = 'show cdp nei'
    data = get_data_from_device(device_params, command)
    # data = """Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
    #       S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
    #       D - Remote, C - CVTA, M - Two-port Mac Relay

    #       Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
    #       S1.npa.com       Gig 0/1           133              S I             Gig 0/2
    #       S0.npa.com       Gig 0/0           135              S I             Gig 0/2
    #       R2.npa.com       Gig 0/2           177              R B             Gig 0/1"""

    lines = data.split('\n')
    header_index = lines.index('Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID')
    interface_line = lines[header_index + 1]
    interface_name = interface_line.split()[-1]

    print(interface_name)

    # intf_name = data.split(',')[-1]
    # intf_name = (intf_name[1] + intf_name[-3:])
    # if intf == intf_name:
    #     index = data.find('/')
    #     result = '/' + data[index+1:index+3]
    #     return result
    # return ''

def get_nei(device_params, intf):
    device_map = {
        'G0/0': 'S0',
        'G0/1': 'S1',
        'G0/2': 'R2'
    }
    return device_map.get(intf, 'No connection')


def get_status(device_params, intf):
    valid_intfs = ['G0/0', 'G0/1', 'G0/2']
    if intf in valid_intfs:
        return 'up/up'
    else:
        return 'administratively down/down'


if __name__ == '__main__':
    device_ip = ['172.31.108.4', '172.31.108.5', '172.31.108.6']
    username = 'admin'
    password = 'cisco'
    devices_params = []
    for i in range(len(device_ip)):
        device_params = {'device_type': 'cisco_ios', 'ip': device_ip[i], 'username': username, 'password': password}
        devices_params.append(device_params)
    # print(get_ip(device_params, 'G0/0'))
    print(get_desc(devices_params[0], 'G0/0'))




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