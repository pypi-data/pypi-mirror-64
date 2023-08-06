"""Networking"""

import socket

def create_simple_tcp_socket_object():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def create_simple_udp_socket_object():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_numeric_ip(ip):
    return socket.gethostbyname(ip)

def check_tcp_port(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    check_if_is_open = sock.connect_ex((ip, port))
    if check_if_is_open == 0:
        return "true [Output: " + str(check_if_is_open) + "]"
    else:
        return "false [Output: " + str(check_if_is_open) + "]"
def check_udp_port(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    check_if_is_open = sock.connect_ex((ip, port))
    if check_if_is_open == 0:
        return "true [Output: " + str(check_if_is_open) + "]"
    else:
        return "false [Output: " + str(check_if_is_open) + "]"