from fabric import Connection

c = Connection('test', user='alexander',
               connect_kwargs={
                   'password': 'test'
               })
result = c.run('uname -s')

print(result)
