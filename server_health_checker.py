import paramiko
import sys
import csv
import datetime
import os
from getpass import getpass
# import bullet

class Server():
    def __init__(self, hostname, user, password):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.ssh_obj = self.connect()
    
    def connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                hostname = self.hostname,
                username = self.user,
                password = self.password
            )
            stdin, stdout, stderr = ssh.exec_command('ls')
            return ssh
        except:
            print('Unable to ssh to the server, please try again')
            ssh.close()
            sys.exit(1)
    
    def get_free_memory(self):
        stdin, stdout, stderr = self.ssh_obj.exec_command('free -h')
        mem_stats = stdout.readlines()[1]
        _, total, used, free, shared, cache, avail = mem_stats.split()
        memory_info = {
                'total': total,
                'used': used,
                'free': free,
                'shared': shared,
                'cache': cache,
                'available': avail
        }
        return memory_info

    def get_logged_in_users(self):
        """
        Should do regex to return/yield the uptime, number of users, load average, and users
        :param ssh_obj:
        :return:
        """
        stdin, stdout, stderr = self.ssh_obj.exec_command('w')
        logged_in = stdout.readlines()
        num_users = len(logged_in) - 2
        return {'logged in users': num_users}

    def _disk_space(self):
        stdin, stdout, stderr = self.ssh_obj.exec_command('df -h /')
        root_space = stdout.readlines()
        disk, total_space, used_space, avail_space, _, _ = root_space[1].split()
        disk_info = {
                'disk_name' : disk,
                'total_space' : total_space,
                'used_space' : used_space,
                'avail_space' : avail_space
        }
        return disk_info

    # def get_stat(self, stat_code):
    #     if stat_code == 'disk_space':
    #         return_dict = _disk_space
    #     elif stats_code == 'logged_in_users':
    #         return_dict = self.get_logged_in_users

    #     for key, value in return_dict.items():
    #         print(f'{key} is : {value}')

    def get_all_stats(self):
        free_mem = self.get_free_memory()
        logged_in_users = self.get_logged_in_users()
        disk_stats = self._disk_space()
        all_stats = {**free_mem, **logged_in_users, **disk_stats}
        return all_stats

    def write_stats_to_csv(self):
        all_stats = self.get_all_stats()
        with open('server_test.csv', 'a', newline='') as csv_file:
            fieldnames = ['Date', 'hostname', 'used mem', 'free mem', 
            'logged in users', 'disk space', 'used space']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if os.path.getsize('server_test.csv') == 0:
                writer.writeheader()
                writer.writerow({'Date': now.strftime('%Y-%m-%d %H:%M'), 
                                'hostname': self.hostname, 
                                'used mem': all_stats['used'],
                                'free mem': all_stats['free'],
                                'logged in users': all_stats['logged in users'],
                                'disk space': all_stats['total_space'],
                                'used space': all_stats['used_space']})
            else:
                writer.writerow({'Date': now.strftime('%Y-%m-%d %H:%M'), 
                                'hostname': self.hostname, 
                                'used mem': all_stats['used'],
                                'free mem': all_stats['free'],
                                'logged in users': all_stats['logged in users'],
                                'disk space': all_stats['total_space'],
                                'used space': all_stats['used_space']})
        self.ssh_obj.close()
    

now = datetime.datetime.now()
# s = Server('206.189.170.174', 'root', 'TestServerPassword1234')
hostname = input('What is the hostname/ip of the server you want to connect to? ')
username = input('What is the username? ')
password = getpass('Enter your password: ')
s = Server(hostname, username, password)
choice = input('Do you want to display all server stats to terminal (y/n)? ')
if choice.lower() == 'y':
    print(s.get_all_stats())
s.write_stats_to_csv()
print('Critical stats written to server_info.csv!')
'''
date/time,hostname,total mem,x,free mem,x,used mem,x
logged in users,x
disk space,x,usedspace,x

1. Write function get_all_stats (CHECK)
2. Finish write to csv function (CHECK)
3. Include try-except in the connect method() (CHECK)
4. Think of CLI flow or use argparse?! (NEED TO DO/BULLET)
5. Query it somehow? (VERSION2)
6. Figure out how to close the ssh connection
7. Why is appending after a line break (DONE)
'''

