import paramiko
import sys
import csv

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.load_system_host_keys(filename=None)

ssh.connect(hostname = '167.99.175.39',
        username = 'root',
        password = 'test123')
        # gss_auth = True,
        # gss_kex = True)


def get_free_memory(ssh_obj):
    """
    returns a dictionary of critical memory stats
    """
    stdin, stdout, stderr = ssh_obj.exec_command('free -h')
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


def get_logged_in_users(ssh_obj):
    """
    Should do regex to return/yield the uptime, number of users, load average, and users
    :param ssh_obj:
    :return:
    """
    stdin, stdout, stderr = ssh_obj.exec_command('w')
    logged_in = stdout.readlines()
    num_users = len(logged_in) - 2
    return num_users

def get_disk_space(ssh_obj):
    stdin, stdout, stderr = ssh_obj.exec_command('df -h /')
    root_space = stdout.readlines()
    disk, total_space, used_space, avail_space, _, _ = root_space[1].split()
    disk_info = {
            'disk_name' : disk,
            'total_space' : total_space,
            'used_space' : used_space,
            'avail_space' : avail_space
    }
    return disk_info

def save_to_csv(mydict):
    # server_csv = open('server_test.csv', 'w')
    # server_csv_writer = csv.DictWriter(server_csv,mydict.keys())
    with open('server_test.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in mydict.items():
            writer.writerow([key + ' mem', value])
        # DICTIONARY COMPREHENSION
    return None


    



print(get_free_memory(ssh))
memory_stats = get_free_memory(ssh)
save_to_csv(memory_stats)
print(get_logged_in_users(ssh))
print(get_disk_space(ssh))

ssh.close()


'''
LEFT TO DO: 
1. Write CSV functions
2. 
hostname,total mem,x,free mem,x,used mem,x
logged in users,x
disk space,x,usedspace, x

1.  Use any data structure like list, dictionary, set or tuple (CHECK)
2.  List comprehension 
3.  Dictionary comprehension
4.  Functions (CHECK)
5.  Classes (CHECK)
6.  User created iterators
7.  Importing external modules (CHECK)
8.  Error checks using try-except (CHECK)
9.  File input and output (CHECK)
10. Regular expression
11. Itertools 
12. Decorators
'''