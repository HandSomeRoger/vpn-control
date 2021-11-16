from django.shortcuts import render
import paramiko
from django.http import HttpResponse, JsonResponse

# ssh_ip = "192.168.149.100"
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

def removeuser(u):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)
    '''拼接shell语句'''
    removeusercmd =

def sshGetAllName():
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)
    '''获取现有的用户信息'''
    stdin, stdout, stderr = ssh_client.exec_command("cat /etc/openvpn/userfile.sh | awk '{print $1}'")

    all1 = str(stdout.read())  # 将stdout.out由bytes类型转化为str类型
    print(all1)
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


def removecrt(u):
    ssh_client = paramiko.SSHClient()

    '''解决目标服务器known_hosts不存在请求者信息的报错'''
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    '''建立ssh连接'''
    ssh_client.connect(hostname=ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password)
    '''拼接grep命令 获取用户所在行数'''
    find_user_id = "grep -nw" + " " + u + " " + "/etc/openvpn/userfile.sh  | awk -F ':' '{print $1}'"
    '''执行grep命令，将获取行数写入uid这个对象'''
    print(find_user_id)
    stdin, stdout, stderr = ssh_client.exec_command(find_user_id)
    '''将标准输出转int，随后转str，因为stdin.write不能接受int数据类型的输入'''
    uid = int(stdout.read())
    uid = str(uid)
    # uid = stdout.read()
    # uid = str(uid)
    # uid = uid[2:-3]
    print(uid)
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
    print(stdout.read())


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':

        user = request.POST.get('username')
        pwd = request.POST.get('password')

        all2 = sshGetAllName()
        print(all2)

        if user == '':
            print("账号不能为空")
            res = {"result": "账号不能为空"}
            return JsonResponse(res, safe=False)

        elif pwd == '':
            print("密码不能为空")
            res = {"result": "密码不能为空"}
            return JsonResponse(res, safe=False)

        elif user in all2:
            print("%s 账号重复!" % user)
            res = {"result": "%s 账号重复!" % user}
            return JsonResponse(res, safe=False)

        else:
            insertuser(user, pwd)
            createcrt(user)
            print("账户开通成功")
            url_address = "http://192.168.31.152/root/" + user + ".ovpn"

            res = {"result": "%s 的账户开通成功!" % user, "url": url_address}
            # print(type(res))

            return JsonResponse(res, safe=False)


def remove_view(request):
    if request.method == 'GET':
        return render(request, 'removeuser.html')
    elif request.method == 'POST':
        user = request.POST.get('username')

        all2 = sshGetAllName()
        print(all2)

        if user == '':
            print("账号不能为空")
            res = {"result": "账号不能为空"}
            return JsonResponse(res, safe=False)

        elif user in all2:
            print("%s 账号已删除" % user)
