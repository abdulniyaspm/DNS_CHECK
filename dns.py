import os
import socket
import subprocess


class DNS:
    """
    A class that finds
    forward dns, backward dns, and ping for a server
    """

    def __init__(self, file_name, path=os.getcwd()):
        """
            >> Will initialise the abspath attribute with the full path of the file name provided.
            >> will raise error if the file name is not found in the specified path.
            >> By default, path would be the same place where this script resides.

        :param file_name:
        :param path:
        """
        self.abs_path = self._find_file_path(file_name, path)
        if not self.abs_path:
            raise IOError("%s not found in %s" % (file_name, path))

    @staticmethod
    def _find_file_path(file_name, path):
        """
        This is function will return the abs path of a file in a specified path.
        :param file_name:
        :param path:
        :return: Abs path of a file.
        """
        for root, dirs, files in os.walk(path):
            if file_name in files:
                return os.path.join(root, file_name)

    def execute(self):
        input_ = self._get_input_from_user()
        data = self._read_from_file()
        {1: self._find_forward_dns,
                2: self._find_reverse_dns,
                3: self._find_ping_response}[input_](data)
        exit(0)

    @staticmethod
    def _find_forward_dns(data):
        """
        Function to find the forward DNS
        """
        for hostname in data:
            try:
                ip = socket.gethostbyname(hostname)
            except (socket.gaierror, socket.herror):
                ip = "No Ip Address"
            print "{0} ---------> {1}".format(hostname, ip)

    @staticmethod
    def _find_reverse_dns(data):
        """
        Function to find the backward DNS
        :param data:
        :return:
        """
        for ip in data:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except (socket.gaierror, socket.herror):
                hostname = "No hostname"

            print "{0} ---------> {1}".format(ip, hostname)

    @staticmethod
    def _find_ping_response(data):
        """
        Function to find the ping response.
        :param data:
        :return:
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
            print "%s is %s" %(hostname_or_ip, ping_status)

    @staticmethod
    def _get_input_from_user():
        # Infinite loop is used here bcz we need to make sure that the user should enter 1, 2, 3.
        # Other than this the prompt will ask again
        while True:
            try:
                input_ = int(raw_input(
                    "Enter 1 ---> Forward DNS \n"
                    "Enter 2 ----> Reverse DNS \n"
                    "Enter 3 ---> Ping Response \n"
                    "Enter Your Input "))
            except ValueError:
                continue

            if input_ in range(1, 5):
                break

        return input_

    def _read_from_file(self):
        """
        Function which return generator object
        :return:
        """
        with open(self.abs_path) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        for line in content:
            yield line.strip()

