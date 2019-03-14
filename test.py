import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname = 'munki-a-1.pnp.melodis.com',
        username = 'root',
        gss_auth = True,
        gss_kex = True)


def get_free_memory(ssh_obj):
    stdin, stdout, stderr = ssh_obj.exec_command('free -h')
    mem_stats = stdout.readlines()[1]
    mem_stats_formatted = " ".join(mem_stats.split())
    return mem_stats_formatted


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
    return root_space[1]


print(get_free_memory(ssh))
print(get_logged_in_users(ssh))
print(get_disk_space(ssh))

ssh.close()


'''
LEFT TO DO: 
1. SPIN UP DIGITAL OCEAN SERVER WITH SSH KEY FOR TESTING
2. TURN THIS INTO A CLASS
3. FIGURE OUT HOW TO RETURN MULTIPLE THINGS FROM THESE FUNCTIONS
'''