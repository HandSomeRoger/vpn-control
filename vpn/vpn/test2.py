import paramiko

ssh_ip = "192.168.149.100"
ssh_port = 22
ssh_username = "root"
ssh_password = "Roger645174748"

def createcrt(u):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)

    '''执行VPN开通脚本'''
    stdin, stdout, stder = ssh_client.exec_command("sh /data/openvpn-install-master/openvpn-install.sh")
    '''输入1，选择新建用户'''
    stdin.write('1\n')
    '''输入新用户用户名'''
    stdin.write(u)
    '''输入回车'''
    stdin.write('\n')
    stdin.flush()
    print(stdout.read())
if __name__ == '__main__':

    createcrt(u="jintian")

