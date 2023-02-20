import os
import argparse
import requests
from github import Github
from pathlib import Path


def get_path_and_filename(content, root_path, out_path):
    d = content.path.replace(root_path, "")
    if d[:1] == "/":
        d = d[1:]
    
    if content.type == "dir":
        return f"{out_path}/{d}", None
    else:
        path, filename = os.path.split(f"{out_path}/{d}")
        return path, filename


def download(url, out_dir, filename):
    if os.path.exists(out_dir) == False:
        Path(out_dir).mkdir(parents=True)

    response = requests.get(url)
    open(f"{out_dir}/{filename}", "wb").write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GitHub Downloader")
    parser.add_argument("repo", nargs=1, type=str, metavar="repo", help="Repository")
    parser.add_argument("root_path", nargs=1, type=str, metavar="root_path", help="Root Path")
    parser.add_argument("out_path", nargs=1, type=str, metavar="out_path", help="Out Path")
    parser.add_argument("access_token", nargs=1, type=str, metavar="access_token", help="Access Token")
    args = parser.parse_args()

    # python github_downloader.py cloim/garage SDWebUI D:\Code\PYTHON\pyGarachi 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
    root_path = args.root_path[0]
    g = Github(args.access_token[0])
    repo = g.get_repo(args.repo[0])
    contents = repo.get_contents(root_path)

    out_path = args.out_path[0]
    while contents:
        file_content = contents.pop(0)
        out_dir, filename = get_path_and_filename(file_content, root_path, out_path)

        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        elif filename is not None:
            download(file_content.download_url, out_dir, filename)
