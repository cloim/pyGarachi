import os
import paramiko
import argparse
from pathlib import Path


def is_folder_or_file(path):
    stat = str(sftp.lstat(path)).split()[0]
    if "d" in stat:
        return "folder"
    else:
        return "file"


def download(src_path, dst_path, recursive):
    if is_folder_or_file(src_path) == "file":
        print(f"{src_path} => {dst_path}")
        path, _ = os.path.split(dst_path)
        if os.path.exists(path) == False:
            Path(path).mkdir(parents=True)
        sftp.get(src_path, f"{dst_path}")
    else:
        if recursive == False:
            return

        dir = sftp.listdir(src_path)
        for path in dir:
            if path == "#recycle":
                continue
            download(f"/{src_path}/{path}", f"{dst_path}/{path}", recursive)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SFTP Downloader")
    parser.add_argument("host", nargs=1, type=str, metavar="host", help="SFTP Host address")
    parser.add_argument("-p", "--port", type=int, help="SFTP Service port")
    parser.add_argument("-u", "--uid", type=str, help="User ID")
    parser.add_argument("-a", "--authkey", type=str, help="Authenticate Key")
    parser.add_argument("-s", "--src", type=str, help="Source")
    parser.add_argument("-d", "--dst", type=str, help="Destination")
    parser.add_argument("-r", "--recursive", type=bool, default=False, help="Recursive")
    args = parser.parse_args()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(args.host[0], args.port, args.uid, args.authkey)
    sftp = ssh.open_sftp()

    download(args.src, args.dst, args.recursive)

    sftp.close()
    ssh.close()
