import os, sys, argparse, json, time
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM


class Client(Thread):
    def __init__(self, host, port, user, absdir):
        super().__init__()
        self.host = host
        self.port = port
        self.user = user            # 用户名空间的名称: to2bage
        self.absdir = absdir        # 上传的绝对路径
        self.client = socket(family=AF_INET, type=SOCK_STREAM)

    def run(self) -> None:
        self.client.connect((self.host, self.port))

        self.client.send("{}".format(self.user).encode("utf8")) # 让远程主机建立用户空间
        self.client.recv(1024)      #  等待确认信号

        for root, dirs, files in os.walk(self.absdir):
            for file in files:
                abs_file_path = os.path.join(root, file)
                index = self.absdir.rfind("/")              # 从右边超找"/"
                relative_file_path = abs_file_path[index+1:]    # 获得文件名或文件夹名, 不包含路径
                print(relative_file_path)
                # 上传relative_file_path的名字, 服务器端开始open文件
                self.client.send(relative_file_path.encode("utf8"))     # 传递文件名
                self.client.recv(1024)      # 等待确认信号
                # 上传abs_file_path文件
                time.sleep(0.3)
                print("开始上传文件: {}".format(relative_file_path))
                num = 0
                filesize = os.path.getsize(abs_file_path)
                with open(abs_file_path, "rb") as fp:
                    for line in fp.readlines():
                        num += len(line)
                        self.client.send(line)
                        print("已经上传了: {:.2f}%".format(num/filesize*100), end="\r", flush=True)
                        self.client.recv(1024)  # 同步服务器
                        pass

                pass
                self.client.send("bye".encode("utf8"))      # 某个文件读取完了
            pass

        self.client.send("bye-bye".encode("utf8"))          # 整个文件夹中的文件都已经上传完毕了





def main():
    parser = argparse.ArgumentParser(
        usage="python3 Client.py --host [主机地址] --port [端口号] --user [用户名] --dir [上传的文件夹的绝对路径]")
    parser.add_argument("--host", dest="host", required=True)
    parser.add_argument("--port", dest="port", required=True)
    parser.add_argument("--user", dest="user", required=True)
    parser.add_argument("--dir", dest="dir", required=True)

    args = parser.parse_args()

    client = Client(host=args.host, port=int(args.port), user=args.user, absdir=args.dir)
    client.start()
    pass


if __name__ == '__main__':
    main()

"""
    python3 Client.py --host 127.0.0.1 --port 8080 --user to2bage --dir /Users/to2bage/downloads/aaa
    self.absdir = /Users/to2bage/downloads/aaa
    
    abs_file_path:
        /Users/to2bage/downloads/aaa/.DS_Store
        /Users/to2bage/downloads/aaa/Untitled3.ipynb
        /Users/to2bage/downloads/aaa/bbb/Untitled3.ipynb
        /Users/to2bage/downloads/aaa/ccc/.DS_Store
        /Users/to2bage/downloads/aaa/ccc/Untitled3.ipynb
        /Users/to2bage/downloads/aaa/ccc/ddd/Untitled3.ipynb
        
    relative_file_path:
        aaa/.DS_Store
        aaa/Untitled3.ipynb
        aaa/bbb/Untitled3.ipynb
        aaa/ccc/.DS_Store
        aaa/ccc/Untitled3.ipynb
        aaa/ccc/ddd/Untitled3.ipynb
    
    python3 Client.py --host 127.0.0.1 --port 8080 --user to2bage --dir /users/apple/downloads/MIUI+12+Wallpapers
"""