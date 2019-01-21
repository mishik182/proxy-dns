class BaseConfig():
    def __init__(self):
        self.dns_address = ('192.168.1.1', 53)
        self.proxy_address = ('192.168.1.100', 53)
        self.domain_black_list = ['ex.ua', 'i.ua']
        self.error_status = b'\x84\x05\x00\x01\x00\x01\x00\x00\x00\x00'
