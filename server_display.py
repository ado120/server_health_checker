import paramiko
import sys

# Input filepath to list of servers in .txt
if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '"file path to server list"')
    sys.exit()

# Open txt file and use a for loop to extract every server in the list
server_file = sys.argv[1]
server_list = []
with open(server_file, 'r') as fo:
    for server in fo:
        # append every server to a list
        server_list.append(server)

print(server_list)

# # Initiate SSH connection to each server in the .txt file
# class SSH:
#     def __init__(self, hostname, username, key):
#         self.hostname = hostname
#         self.username = username
#         self.key = key
#
#     def