import paramiko
import os

class SSHDialog:
    def __init__(self, hostname:str, ip:str, pkey_path:str, timeout=30):
        self.hostname = hostname
        self.ip = ip
        pkey = paramiko.RSAKey.from_private_key_file(pkey_path)
        trans = paramiko.Transport((ip, 22))
        trans.connect(username=hostname, pkey=pkey)
        self.ssh = paramiko.SSHClient()
        self.ssh._transport = trans
        self.sftp = paramiko.SFTPClient.from_transport(trans)

    def exec_command(self, command:str, print_out=True, verbose=False):
        try:
            __ , stdout, stderr = self.ssh.exec_command(command)
        except paramiko.ssh_exception.SSHException:
            print("Catch Exception: SSHException")
            print("Fail to excute command")
            return None
        else:
            stdout_string = stdout.read().decode('utf-8')
            stderr_string = stderr.read().decode('utf-8')
            if(stdout_string): 
                if(print_out):
                    print("[{hostname}@{ip}]".format(hostname=self.hostname, ip=self.ip), '[stdout]:', stdout_string)
                return stdout_string
            if(stderr_string): 
                if(print_out):
                    print("[{hostname}@{ip}]".format(hostname=self.hostname, ip=self.ip), '[stderr]:', stderr_string)
                return stderr_string
    
    def send_file(self, local_path:str, remote_path:str):
        try:
            self.sftp.put(local_path, remote_path)
            print("[upload]:", local_path)
        except FileNotFoundError:
            print('[FileNotFoundError]: {file}'.format(file=local_path))

    def send_folder(self, local_path:str, remote_path:str, auto_makedirs=True):
        try:
            localfiles = os.listdir(local_path)
        except FileNotFoundError:
            print('[FileNotFoundError]: {path}'.format(path=local_path))
            return None
        else:
            if (auto_makedirs):
                # 递归地创建目录
                self.exec_command("mkdir -p {dir}".format(dir=remote_path), print_out=False)
            for filename in localfiles:
                filepath_local = os.path.join(local_path, filename)
                filepath_remote = os.path.join(remote_path, filename)
                # 需要传的是文件夹
                if(os.path.isdir(filepath_local)):
                    # 递归创建文件夹
                    self.send_folder(filepath_local, filepath_remote)
                else:
                    # 需要传的是文件
                    try:
                        self.sftp.put(filepath_local, filepath_remote)
                        print("[upload][recursive]:", filepath_local)
                    except FileNotFoundError:
                        print("file/path not found: {file}".format(file=filepath_remote))
                        print("have a try to set 'auto_makedirs' to 'true' ")
                        return False
            return True


        



        