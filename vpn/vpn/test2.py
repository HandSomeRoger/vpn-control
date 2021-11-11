import paramiko

sshinfo = "hostname='192.168.149.100', port=22, username='root', password='Roger645174748'"

def insertuser(u,p):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    print(sshinfo)
    ssh_client.connect(sshinfo)
    '''拼接shell语句'''
    insertusercmd = "echo " + u + " " + p + ">> /tmp/test"
    ssh_client.exec_command(insertusercmd)

if __name__ == '__main__':

    insertuser(u="luojie222", p="luojie222")