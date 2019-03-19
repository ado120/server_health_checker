import paramiko
import sys
import csv
import datetime

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
        with open('server_test.csv', 'w') as csv_file:
            fieldnames = ['Date', 'hostname', 'used mem', 'free mem', 
            'logged in users', 'disk space', 'used space']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            # FOR LOOP HERE FOR WRITER.WRITEROW()
            writer.writerow({'Date': now.strftime('%Y-%m-%d %H:%M'), 
                            'hostname': self.hostname, 
                            'used mem': all_stats['used'],
                            'free mem': all_stats['free'],
                            'logged in users': all_stats['logged in users'],
                            'disk space': all_stats['total_space'],
                            'used space': all_stats['used_space']})

now = datetime.datetime.now()
s = Server('167.99.175.41', 'root', 'test123')
t = s.get_free_memory()
logged_in_users = s.get_logged_in_users()
# s._disk_space()
# s.write_mem_to_csv()
# print(s)
# print(t)
print(s.get_all_stats())
s.write_stats_to_csv()
'''
date/time,hostname,total mem,x,free mem,x,used mem,x
logged in users,x
disk space,x,usedspace,x

1. Write function get_all_stats (CHECK)
2. Finish write to csv function (IN PROGRESS)
3. Include try-except in the connect method() (CHECK, make it re-run the script and not exit)
4. Think of CLI flow or use argparse?! (NEED TO DO)
5. Query it somehow?
'''

