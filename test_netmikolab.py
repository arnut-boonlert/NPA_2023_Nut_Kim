from netmikolab import *

device_ip = '172.31.108.4'
username = 'admin'
password = 'cisco'
device_params = {'device_type': 'cisco_ios', 'ip': device_ip, 'username': username, 'password': password}


def test_ip():
    assert get_ip(device_params, 'G0/0') == '172.31.108.4'
    assert get_nei(device_params, 'G0/0') == 'S0'
    assert get_status(device_params, 'G0/0') == 'up/up'
    
    assert get_status(device_params, 'G0/1') == '172.31.108.17'
    print("All passed")

if __name__ == '__main__':
    test_ip()
