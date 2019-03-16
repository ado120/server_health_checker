import paramiko

class Server():
    def __init__(self, hostname, user):
        self.hostname = hostname
        self.user = user
