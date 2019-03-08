import paramiko

transport = paramiko.Transport('10.0.0.112', 22)
transport.connect(username='fa', password='fa')

sftp = paramiko.SFTPClient.from_transport(transport)

sftp.get('/home/arm/1/scp_test.txt', '/home/arm/python/scp_test.txt')
# 将Linux上的/root/Linux.txt下载到本地

transport.close()
