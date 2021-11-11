import paramiko

ssh_ip = "192.168.149.100"
ssh_port = 22
ssh_username = "root"
ssh_password = "Roger645174748"

def insertuser(u,p):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''

    #ssh_client.connect(hostname="192.168.149.100", port=22, username="root", password="Roger645174748")
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)
    '''拼接shell语句'''
    insertusercmd = "echo " + u + " " + p + ">> /tmp/test"
    ssh_client.exec_command(insertusercmd)

if __name__ == '__main__':

    insertuser(u="luojie23", p="luojie22")