import paramiko

ssh_ip = "192.168.31.152"
ssh_port = 22
ssh_username = "root"
ssh_password = "Roger645174748"

def removecrt(u):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)
    '''拼接grep命令 获取用户所在行数'''
    find_user_id = "grep -nw" + " " + u + " " + "/etc/openvpn/userfile.sh  | awk -F ':' '{print $1}'"
    '''执行grep命令，将获取行数写入uid这个对象'''
    print("查找语句为" + find_user_id)
    stdin, stdout, stderr = ssh_client.exec_command(find_user_id)
    '''将标准输出转int，随后转str，因为stdin.write不能接受int数据类型的输入'''
    uid = int(stdout.read())
    uid = str(uid)
    # uid = stdout.read()
    # uid = str(uid)
    # uid = uid[2:-3]
    print(u + "的uid为" + uid)
    '''执行服务器上的删除用户的交互式脚本'''
    stdin, stdout, stderr = ssh_client.exec_command("sh /data/openvpn-install-master/openvpn-install.sh")
    '''输入2，选择删除用户'''
    stdin.write('2\n')
    '''输入要删除的用户的用户名id'''
    stdin.write(uid)
    stdin.write('\n')
    '''输入y并且回车'''
    stdin.write('y\n')
    stdin.flush()






if __name__ == '__main__':
    removecrt(u="luojie008")

