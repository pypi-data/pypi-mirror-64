import sys
import os
import shutil

from serverD.conf import *

file_path = os.path.abspath(os.path.dirname(__file__))

server_base_data = {

    "serverPut": "{user} {host} {pwd} {port} {locPath} {serPath}",
    "serverGet": "{user} {host} {pwd} {port} {locPath} {serPath}",
    "serverLogin": "{user} {host} {pwd} {port}",
    "serverTbj": "{user} {host} {pwd} {port} {pem}",

}

class ServerD:

    @staticmethod
    def serverB(s_type, s_data):
        cmd = '{}/serverE/{} {}'.format(file_path, s_type, s_data)
        print(cmd)
        os.system(cmd)

    def login(self, server_name):
        s_type = "serverLogin"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        login_dict = server_dict.get(server_name)
        if not login_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        s_data = server_base_data.get(s_type).format(**login_dict)
        self.serverB(s_type, s_data)

    def get(self, server_name, locPath, serPath, root=False):
        s_type = "serverGet"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        get_dict = server_dict.get(server_name)
        if not get_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        if root:
            get_dict.update({"locPath": locPath, "serPath": serPath, "user": 'root', "pwd": root_pwd})
        else:
            get_dict.update({"locPath": locPath, "serPath": serPath})
        s_data = server_base_data.get(s_type).format(**get_dict)
        self.serverB(s_type, s_data)

    def put(self, server_name, locPath, serPath, root=False):
        s_type = "serverPut"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        get_dict = server_dict.get(server_name)
        if not get_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        if root:
            get_dict.update({"locPath": locPath, "serPath": serPath, "user": 'root', "pwd": root_pwd})
        else:
            get_dict.update({"locPath": locPath, "serPath": serPath})
        s_data = server_base_data.get(s_type).format(**get_dict)
        self.serverB(s_type, s_data)

    def loginRoot(self, server_name):
        s_type = "serverLogin"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        login_dict = server_dict.get(server_name)
        if not login_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        login_dict["user"] = "root"
        login_dict["pwd"] = root_pwd
        s_data = server_base_data.get(s_type).format(**login_dict)
        self.serverB(s_type, s_data)

    def loginTbj(self, pwd):
        """
        :param server_name:
        :return:
        """
        s_type = "serverTbj"
        login_dict = server_dict.get("tbj")
        login_dict["pwd"] = pwd
        s_data = server_base_data.get(s_type).format(**login_dict)
        self.serverB(s_type, s_data)

    def main(self, server):
        try:
            if server:
                if server == "tbj":
                    try:
                        self.loginTbj(sys.argv[2])
                    except IndexError:
                        print("请输入正确格式: go tbj password")
                elif server == "root":
                    try:
                        self.loginRoot(sys.argv[2])
                    except IndexError:
                        print("请输入正确格式 go root server: 如: go root 429")

                elif server == "get":
                    try:
                        if sys.argv[1] == "root":
                            server_name = sys.argv[2]
                            serPath = sys.argv[3]
                            locPath = sys.argv[4]
                            self.get(server_name, locPath, serPath, root=True)
                        else:
                            server_name = sys.argv[1]
                            serPath = sys.argv[2]
                            locPath = sys.argv[3]
                            self.get(server_name, locPath, serPath)
                    except IndexError:
                        print("输入参数错误!!!\n正确示例 >>> get [root] <服务器名称> <服务器文件路径> <本地文件路径>")

                elif server == "put":
                    try:
                        if sys.argv[1] == "root":
                            server_name = sys.argv[2]
                            serPath = sys.argv[3]
                            locPath = sys.argv[4]
                            self.put(server_name, locPath, serPath, root=True)
                        else:
                            server_name = sys.argv[1]
                            serPath = sys.argv[2]
                            locPath = sys.argv[3]
                            self.put(server_name, locPath, serPath)
                    except IndexError:
                        print("输入参数错误!!!\n正确示例 >>> put [root] <服务器名称> <服务器文件路径> <本地文件路径>")

                else:
                    server_name = "{}".format(server)
                    print("正在登录{}...".format(server_name))
                    self.login(server_name)
            else:
                print("请输入服务器编号")
        except IndexError:
            print("输入参数错误!!!\n正确示例 >>>  go [登录类型] <服务器名称> ")


def main():
    try:
        base_server = sys.argv[1]
        sd = ServerD()
        sd.main(base_server)
    except IndexError:
        print("参数异常: 正确格式如下:{}{}".format("go <服务器名称>\n",
                                         "go root <服务器名称>\n",
                                         "go tbj <密码>\n",
                                         "put <服务器名称> <服务器文件路径> <本地文件路径>\n",
                                         "get <服务器名称> <服务器文件路径> <本地文件路径>\n",
                                         ))


def get():
    try:
        base_server = "get"
        sd = ServerD()
        sd.main(base_server)
    except IndexError:
        print("参数异常: 正确格式如下:{}{}".format(
            "go <服务器名称>\n",
            "go root <服务器名称>\n",
            "go tbj <密码>\n",
            "put <服务器名称> <服务器文件路径> <本地文件路径>\n",
            "get <服务器名称> <服务器文件路径> <本地文件路径>\n",
        ))


def put():
    try:
        base_server = "put"
        sd = ServerD()
        sd.main(base_server)
    except IndexError:
        print("参数异常: 正确格式如下:{}{}".format(
            "go <服务器名称>\n",
            "go root <服务器名称>\n",
            "go tbj <密码>\n",
            "put <服务器名称> <服务器文件路径> <本地文件路径>\n",
            "get <服务器名称> <服务器文件路径> <本地文件路径>\n",
        ))


def update_conf():
    try:
        new_conf_path = sys.argv[1]
        if os.path.exists(new_conf_path):
            shutil.copy(new_conf_path, "{}/conf.py".format(file_path))
        else:
            print("该文件不存在: {}".format(new_conf_path))
    except IndexError:
        print("updateConf <当前配置文件路径>\n 查看demo 可执行 cat {}/conf_demo.py ".format(file_path))

if __name__ == '__main__':
    main()
