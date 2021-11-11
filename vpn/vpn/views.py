import json

from django.shortcuts import render
import paramiko
from django.http import HttpResponse

#ssh_ip = "192.168.149.100"
ssh_ip = "192.168.31.152"
ssh_port = 22
ssh_username = "root"
ssh_password = "Roger645174748"


def insertuser(u, p):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)
    '''拼接shell语句'''
    insertusercmd = "echo " + u + " " + p + " " ">> /tmp/test"
    ssh_client.exec_command(insertusercmd)


def sshGetAllName():
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)
    '''获取现有的用户信息'''
    stdin, stdout, stderr = ssh_client.exec_command("cat /tmp/test | awk '{print $1}'")

    all1 = str(stdout.read())  # 将stdout.out由bytes类型转化为str类型
    all1 = all1[2:-1]  # 输出左边第二位到右边的第一位之间的字符
    all2 = all1.split('\\n')  # 根据\n切割字符，形成数组
    return all2


def createcrt(u):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)

    '''执行VPN开通脚本'''
    stdin, stdout, stderr = ssh_client.exec_command("sh /data/openvpn-install-master/openvpn-install.sh")
    '''输入1，选择新建用户'''
    stdin.write('1\n')
    '''输入新用户用户名'''
    stdin.write(u)
    '''输入回车'''
    stdin.write('\n')
    stdin.flush()
    print(stdout.read())


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':

        user = request.POST.get('username')
        pwd = request.POST.get('password')

        all2 = sshGetAllName()
        print(all2)

        if user in all2:
            print("账号重复")
            # return HttpResponse("%s 账号重复!" % user)
            return HttpResponse(json.dumps(all2))
        elif pwd == '':
            print("密码不能为空")
            return HttpResponse("%s 的密码不能为空!" % user)

        else:
            insertuser(user, pwd)
            createcrt(user)
            print("账户开通成功")
            return HttpResponse("%s 的账户开通成功!" % user)
