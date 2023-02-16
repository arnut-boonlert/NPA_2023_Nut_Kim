from netmikolab import *

devices_ip = ['172.31.108.4', '172.31.108.5', '172.31.108.6']
username = 'admin'
password = 'cisco'
devices_params = []
for i in range(len(devices_ip)):
    device_params = {'device_type': 'cisco_ios', 'ip': devices_ip[i], 'username': username, 'password': password}
    devices_params.append(device_params)
print(devices_params[1])

def test_ip():
    assert get_ip(devices_params[0], 'G0/0') == '172.31.108.4'
    # assert get_ip(devices_params[0], 'G0/1') == '172.31.108.17'
    # assert get_ip(devices_params[0], 'G0/2') == '172.31.108.33'
    # assert get_ip(devices_params[0], 'G0/3') == 'unassigned'
    print("All passed")

if __name__ == '__main__':
    test_ip()










    
    
    # assert get_status(devices_params[0], 'G0/0') == 'up/up'


    # assert get_mask(devices_params[0], 'G0/1') == '/28'
    # assert get_des(devices_params[0], 'G0/0') == 'Connect to G0/2 of S1'
    # assert get_status(devices_params[0], 'G0/1') == 'up/up'

    
    # assert get_mask(devices_params[0], 'G0/2') == '/28'
    # assert get_des(devices_params[0], 'G0/0') == 'Connect to G0/2 of R2'
    # assert get_status(devices_params[0], 'G0/2') == 'up/up'

    
    # assert get_status(devices_params[0], 'G0/3') == 'admin down/down'
    # assert get_ip(devices_params[1], 'G0/0') == '172.31.108.5'
    # assert get_mask(devices_params[1], 'G0/0') == 'S0'
    # assert get_status(devices_params[1], 'G0/0') == 'up/up'