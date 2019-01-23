import socket
from dns_proxy_cfg import BaseConfig


class ProxyServer(BaseConfig):
    proxy = None

    def get_domain_name(self, request):
        domain_name = ''
        for byte in request[12:]:
            char = chr(byte)
            if char.isalpha() or char.isdigit():
                domain_name += char
            else:
                if char in '-':
                    domain_name += char
                    continue
                domain_name += '.'
                if len(domain_name) > 2:
                    if domain_name[-4:-2] == '..':
                        return domain_name[1:-4]

    def is_blocked_domain(self, domain_name):
        return True if domain_name in self.domain_black_list else False

    # SEND RESPONSE TO A CLIENT
    def send_response(self, request, address):
        if self.is_blocked_domain(self.get_domain_name(request)):
            data = request[:2] + self.error_status
            self.proxy.sendto(data, address)
            return
        self.send_request(request, address)

    # SEND REQUEST TO DNS SERVER
    def send_request(self, request, address):
        dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns.sendto(request, self.dns_address)
        response, _ = dns.recvfrom(512)
        self.proxy.sendto(response, address)

    def start_proxy(self):
        self.proxy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.proxy.bind(self.proxy_address)
        while True:
            # READ 512 OCTETS
            try:
                request, address = self.proxy.recvfrom(512)
                self.send_response(request, address)
            except Exception as e:
                print('Exception ', e)


ProxyServer().start_proxy()
