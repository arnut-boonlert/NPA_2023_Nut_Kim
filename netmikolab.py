from netmiko import ConnectHandler
import re
import textfsm

def send_command(device_params, commands):
    with ConnectHandler(**device_params) as ssh:
        for command in commands:
            ssh.send_command(command, expect_string=r"\S+#")

def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command(command, use_textfsm=True)
    return result

def get_ip(device_params, intf):
    command = 'sh ip int br'
    result = get_data_from_device(device_params, command)
    for i in range(len(result)):
        local_intf = result[i]['intf'][0]+result[i]['intf'][-3:]
        if local_intf == intf:
            return result[i]['ipaddr']

def get_cdp_nei(device_params, intf):
    command = 'show cdp nei'
    result = get_data_from_device(device_params, command)
    with open("cdp.template") as template: #cdp.template returned list of lists
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(result)
    for i in range(len(result)):
        local_intf = result[i][1][0]+result[i][1][-3:]
        if local_intf == intf:
            device_id = result[i][0][:2]
            port_id_type = result[i][3][0]
            port_id_num = result[i][4]
            port_id = port_id_type+port_id_num
            return f'Connect to {port_id} of {device_id}'
        elif i == len(result)-1:
            return 'Not Use'

def set_desc(device_params, intf):
    commands = ['conf t', f'int {intf}', f'des {get_cdp_nei(device_params, intf)}', 'end']
    send_command(device_params, commands)

def get_only_desc(device_params):
    command = 'show int des'
    result = get_data_from_device(device_params, command)
    return result

def get_desc(device_params, intf, skip_get_desc='True'):#let skip_get_desc=True because intfaces description have configured
    if not skip_get_desc:
        set_desc(device_params, intf)
    result = get_only_desc(device_params)
    for i in range(len(result)):
        local_intf = result[i]['port'][0]+result[i]['port'][-3:]
        intf_desc = result[i]['descrip']
        if local_intf == intf:
            return intf_desc

def get_status(device_params, intf):
    result = get_only_desc(device_params)
    for i in range(len(result)):
        local_intf = result[i]['port'][0]+result[i]['port'][-3:]
        proto = result[i]['protocol']
        status = result[i]['status']
        if local_intf == intf:
            intf_status = f'{status} {proto}'
            return intf_status
    

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
    print(get_status(devices_params[0], 'G0/0'))

