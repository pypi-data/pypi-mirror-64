pwd = ""
root_pwd = ""
tbj_pem = "pem文件路径"

server_base_data = {

    "serverPut": "{user} {host} {pwd} {port} {locPath} {serPath}",
    "serverGet": "{user} {host} {pwd} {port} {locPath} {serPath}",
    "serverLogin": "{user} {host} {pwd} {port}",
    "serverTbj": "{user} {host} {pwd} {port} {pem}",

}
server_dict = {
    "vpc实例名称": {"host": "外网地址", "user": "用户名", "port": "端口号", "pwd": "密码"},
    "tbj": {"host": "", "user": "", "port": "22", "pwd": "", "pem": tbj_pem},
    "233": {"host": "", "user": "", "port": "22", "pwd": ""},
}


if __name__ == '__main__':
    print(str(server_dict))
