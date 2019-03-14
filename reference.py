import paramiko
import gssapi
import sys
import subprocess


if len(sys.argv) != 2:
    print(f'Usage {sys.argv[0]} "line to add"')
    sys.exit()

passed_argument = sys.argv[1].strip()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname = 'afs1.pnp.melodis.com',
        username = 'root',
        gss_auth = True,
        gss_kex = True)

ssh.exec_command(f'cd /melodis/ldap && echo {passed_argument} >> passwd')
print(passed_argument)
stdin, stdout, stderr = ssh.exec_command('cd /melodis/ldap && tail -n 10 passwd')

stdin1, stdout1, stderr1 = ssh.exec_command('cd /melodis/ldap && ./rebuildldapdb')
exit_status = stdout1.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print (stdout1.readlines())
else:
    print("Error", exit_status)

print(stdout.readlines())

ssh.close()
print('User has been successfully on-boarded!')