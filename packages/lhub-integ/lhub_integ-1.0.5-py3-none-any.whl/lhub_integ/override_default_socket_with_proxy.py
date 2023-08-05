import urllib.request, urllib.parse, urllib.error
import socks
import socket
import os

# If socks_proxy is set in environment variable then,
# this script replaces the default socket to route through
# socks proxy

DEFAULT_SOCKET = socket.socket


def get_proxy():
    proxy = os.environ.get('socks_proxy')
    if proxy:
        _, host = urllib.parse.splittype(proxy)  # _: socks5, host: //localhost-raservice:0001
        host, _ = urllib.parse.splithost(host)  # host: localhost-raservice:0001, _: ''
        host, port = urllib.parse.splitport(host)  # host: localhost-raservice, port: '0001'
        port = int(port)
        if host and port:
            return host, port
        return None
    else:
        return None


def override_socket():
    proxy_settings = get_proxy()
    if proxy_settings:
        host, port = proxy_settings
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
        socket.socket = socks.socksocket


def remove_socket_override():
    socket.socket = DEFAULT_SOCKET


override_socket()
