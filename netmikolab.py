from netmiko import ConnectHandler
import paramiko



def get_data_from_device(device_params):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command('sh ip int br')
        return result_shipintbr


def get_ip(device_params, intf):
    print('hello')


if __name__ == '__main__':
    device_ip = '172.31.108.4'
    username = 'admin'
    password = 'cisco'
    device_params = {'device_type': 'cisco_ios', 'ip': device_ip, 'username': username, 'password': password}
    print(get_ip(device_params, 'G0/0'))
