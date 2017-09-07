import os
import socket
import subprocess


def get_forward_dns(servers):
    """
        >> Function to get the forward DNS of a hostname.
        >> get_forward_dns("www.google.com")
        >> 123.143.543.234

    :param servers: collection of hostname
    :return: Ip corresponds to hostname
    """
    for hostname in servers:
        try:
            ip = socket.gethostbyname(hostname)
        except (socket.gaierror, socket.herror):
            ip = "No Ip Address"

        yield (hostname, ip)


def get_reverse_dns(ips):
    """
        >> To get the reverse DNS of a IP
        >> get_reverse_dns("123.143.543.234")
        >> www.google.com

    :param ips: collection of IPs
    :return: Hostname corresponds to IP
    """
    for ip in ips:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except (socket.gaierror, socket.herror):
            hostname = "No hostname"

        yield (ip, hostname)


def find_ping_response(data):
    """
        >> To find the server is active or not.
        >> find_ping_response("www.google.com")
        >> Active

    :param data: Collection of Ip or hostname
    :return: Return Active or Unreachable
    """
    for hostname_or_ip in data:
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', '-c', '3', hostname_or_ip],
                    stdout=DEVNULL,  # suppress output
                    stderr=DEVNULL
                )
                ping_status = "Active"
            except subprocess.CalledProcessError:
                ping_status = "Unreachable"

        yield (hostname_or_ip, ping_status)



def find_forward_backward_ping(server_name):
    """
    To find all the details.
    :param servers:
    :return:
    """

    forward_dns = get_forward_dns([server_name]).next()
    if forward_dns[1] != "No Ip Address":
        backward_dns = get_reverse_dns([forward_dns[1]]).next()[1]

    else:
        backward_dns = "No Forward DNS"

    is_both_forward_backward_same, ping = server_name.lower() == backward_dns, find_ping_response([server_name]).next()[
        1]

    return forward_dns[1], backward_dns, is_both_forward_backward_same, ping