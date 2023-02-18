import pytest
from netmikolab import *


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

@pytest.mark.ip
def test_ip():
    assert get_ip(devices_params[0], 'G0/0') == '172.31.108.4'
    assert get_ip(devices_params[0], 'G0/1') == '172.31.108.17'
    assert get_ip(devices_params[0], 'G0/2') == '172.31.108.33'
    assert get_ip(devices_params[0], 'G0/3') == 'unassigned'
    assert get_ip(devices_params[1], 'G0/0') == '172.31.108.5'
    assert get_ip(devices_params[1], 'G0/1') == '172.31.108.34'
    assert get_ip(devices_params[1], 'G0/2') == '172.31.108.49'
    assert get_ip(devices_params[1], 'G0/3') == 'unassigned'
    assert get_ip(devices_params[2], 'G0/0') == '172.31.108.6'
    assert get_ip(devices_params[2], 'G0/1') == '172.31.108.50'
    assert get_ip(devices_params[2], 'G0/2') == '192.168.122.112'
    assert get_ip(devices_params[2], 'G0/3') == 'unassigned'
    print("All passed")

@pytest.mark.cabled
def test_cabled():
    assert get_cdp_nei(devices_params[0], 'G0/0') == 'Connect to G0/2 of S0'
    assert get_cdp_nei(devices_params[0], 'G0/1') == 'Connect to G0/2 of S1'
    assert get_cdp_nei(devices_params[0], 'G0/2') == 'Connect to G0/1 of R2'
    assert get_cdp_nei(devices_params[0], 'G0/3') == 'Not Use'
    assert get_cdp_nei(devices_params[1], 'G0/0') == 'Connect to G0/3 of S0'
    assert get_cdp_nei(devices_params[1], 'G0/1') == 'Connect to G0/2 of R1'
    assert get_cdp_nei(devices_params[1], 'G0/2') == 'Connect to G0/1 of R3'
    assert get_cdp_nei(devices_params[1], 'G0/3') == 'Not Use'
    assert get_cdp_nei(devices_params[2], 'G0/0') == 'Connect to G1/0 of S0'
    assert get_cdp_nei(devices_params[2], 'G0/1') == 'Connect to G0/2 of R2'
    assert get_cdp_nei(devices_params[2], 'G0/2') == 'Connect to G0/3 of R3'
    assert get_cdp_nei(devices_params[2], 'G0/3') == 'Not Use'

@pytest.mark.desc
def test_desc():
    assert get_desc(devices_params[0], 'G0/0') == 'Connect to G0/2 of S0'
    assert get_desc(devices_params[0], 'G0/1') == 'Connect to G0/2 of S1'
    assert get_desc(devices_params[0], 'G0/2') == 'Connect to G0/1 of R2'
    assert get_desc(devices_params[0], 'G0/3') == 'Not Use'
    assert get_desc(devices_params[1], 'G0/0') == 'Connect to G0/3 of S0'
    assert get_desc(devices_params[1], 'G0/1') == 'Connect to G0/2 of R1'
    assert get_desc(devices_params[1], 'G0/2') == 'Connect to G0/1 of R3'
    assert get_desc(devices_params[1], 'G0/3') == 'Not Use'
    assert get_desc(devices_params[2], 'G0/0') == 'Connect to G1/0 of S0'
    assert get_desc(devices_params[2], 'G0/1') == 'Connect to G0/2 of R2'
    assert get_desc(devices_params[2], 'G0/2') == 'Connect to G0/3 of R3'
    assert get_desc(devices_params[2], 'G0/3') == 'Not Use'


@pytest.mark.status
def test_status():
    assert get_status(devices_params[0], 'G0/0') == 'up up'
    assert get_status(devices_params[0], 'G0/1') == 'up up'
    assert get_status(devices_params[0], 'G0/1') == 'up up'
    assert get_status(devices_params[0], 'G0/3') == 'admin down down'


if __name__ == '__main__':
    test_ip()
    test_cabled()
    test_desc()