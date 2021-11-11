from django.shortcuts import render
import paramiko
import tkinter
import tkinter.messagebox
from django.http import HttpResponse





sshinfo = "hostname='192.168.149.100', port=22, username='root', password='Roger645174748'"




def insertuser(u, p):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname="192.168.31.152", port=22, username="root", password="Roger645174748")
    '''拼接shell语句'''
    insertusercmd = "echo " + u + " " + p + " " ">> /tmp/test"
    ssh_client.exec_command(insertusercmd)


def sshGetAllName():
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname="192.168.31.152", port=22, username="root", password="Roger645174748")
    '''获取现有的用户信息'''
    stdin, stdout, stderr = ssh_client.exec_command("cat /tmp/test | awk '{print $1}'")

    all1 = str(stdout.read())  # 将stdout.out由bytes类型转化为str类型
    all1 = all1[2:-1]          # 输出左边第二位到右边的第一位之间的字符
    all2 = all1.split('\\n')   # 根据\n切割字符，形成数组
    return all2


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
            return HttpResponse("%s 账号重复!" % user)
            #return render(request, 'register.html')
        elif pwd == '':
            print("密码不能为空")
            return HttpResponse("%s 的密码不能为空!" % user)
        else:
            insertuser(user, pwd)
            print("账户开通成功")
            return HttpResponse("%s 的账户开通成功!" % user)



