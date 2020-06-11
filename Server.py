import os, sys, argparse, json
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM


class Server(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server = socket(family=AF_INET, type=SOCK_STREAM)
        self.root = "/Users/apple"
        self._start()

    def _start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print("Server is listening at port: {}".format(self.port))

    def run(self) -> None:
        while True:
            client, addr = self.server.accept()
            print("Welcome: {}".format(addr))

            work = Thread(target=self._handle_client, args=(client, addr))
            work.start()
            pass
        pass

    def _handle_client(self, client, addr):
        data = client.recv(1024).decode("utf8")   # 获得用户名空间的名字
        print(data)
        temp_root = os.path.join(self.root, data) # 获得用户名空间的绝对路径: /Users/to2bage/to2bage, 注意: 不能修改self.root
        client.send("ok".encode("utf8"))          # 再获得用户名空间的名字之后, 返回应答信息



        while True:
            file_name = client.recv(1024).decode("utf8")  # 获得文件名: aaa/bbb/Untitled3.ipynb
            if file_name == "bye-bye":
                break
            print(file_name)
            client.send("ok".encode("utf8"))  # 获得文件名后, 返回应答信息

            # 创建必要的目录
            index = file_name.rfind("/")
            filename = file_name[index + 1:]  # Untitled3.ipynb
            filepath = file_name[:index]  # aaa/bbb
            abs_file_path = os.path.join(temp_root, filepath)  # /Users/to2bage/to2bage/aaa/bbb
            if not os.path.exists(abs_file_path):
                os.makedirs(abs_file_path)  # 路径不存在, 就创建
            abs_file_path = os.path.join(abs_file_path, filename)  # /Users/to2bage/to2bage/aaa/bbb/Untitled3.ipynb
            # 开始接受上传文件的内容
            with open(abs_file_path, "wb") as fb:
                while True:
                    data = client.recv(1024)
                    if data == b"bye":  # 获得bye, 表示上传完毕
                        break
                    fb.write(data)
                    client.send("ok".encode("utf8"))
                pass
            print("{}上传完毕!!!".format(abs_file_path))

        print("文件夹中的文件都已经上传完毕了...")
        pass

    pass


def main():
    parser = argparse.ArgumentParser(
        usage="python3 Client.py --host [主机地址] --port [端口号]")
    parser.add_argument("--host", dest="host", required=True)
    parser.add_argument("--port", dest="port", required=True)

    args = parser.parse_args()

    server = Server(host=args.host, port=int(args.port))
    server.start()
    pass


if __name__ == '__main__':
    main()