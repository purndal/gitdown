#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse

"""
GitHub Directory Downloader (gitdown.py) - Folder Version
--------------------------------------------------------
이 스크립트는 GitHub 저장소의 특정 폴더를 내 컴퓨터에 직접 다운로드합니다.
ZIP 압축 없이 폴더 구조 그대로 파일을 저장합니다.

사용법:
    python gitdown.py [GitHub_URL]

예시:
    python gitdown.py https://github.com/MinhasKamal/DownGit/tree/master/res
"""

def parse_github_url(url):
    """URL에서 사용자, 레포지토리, 브랜치, 경로를 파싱합니다."""
    parsed = urllib.parse.urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    
    if len(path_parts) < 2:
        raise ValueError("올바른 GitHub URL이 아닙니다.")
    
    owner = path_parts[0]
    repo = path_parts[1]
    branch = "main" # 기본값
    folder_path = ""
    
    if len(path_parts) > 3 and path_parts[2] == "tree":
        branch = path_parts[3]
        folder_path = "/".join(path_parts[4:])
    elif len(path_parts) > 3 and path_parts[2] == "blob":
        branch = path_parts[3]
        folder_path = "/".join(path_parts[4:])
    
    return {
        "owner": owner,
        "repo": repo,
        "branch": branch,
        "path": folder_path,
        "name": path_parts[-1] if folder_path else repo
    }

def get_github_contents(owner, repo, path, branch):
    """GitHub API를 사용하여 파일 목록을 가져옵니다."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    
    headers = {
        "User-Agent": "GitDown-CLI-Agent"
    }
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    req = urllib.request.Request(api_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching contents: {e}")
        return None

def download_item(owner, repo, path, branch, local_base_dir, remote_base_path):
    """항목(파일/디렉토리)을 재귀적으로 다운로드합니다."""
    contents = get_github_contents(owner, repo, path, branch)
    if not contents:
        return

    if isinstance(contents, dict):
        contents = [contents]

    for item in contents:
        # 로컬 저장 경로 계산
        relative_path = os.path.relpath(item["path"], remote_base_path)
        local_path = os.path.join(local_base_dir, relative_path)

        if item["type"] == "dir":
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            download_item(owner, repo, item["path"], branch, local_base_dir, remote_base_path)
        else:
            print(f"Downloading: {item['path']} -> {local_path}")
            # 폴더가 없으면 생성
            dir_name = os.path.dirname(local_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                
            file_req = urllib.request.Request(item["download_url"], headers={"User-Agent": "GitDown-CLI-Agent"})
            try:
                with urllib.request.urlopen(file_req) as response:
                    file_data = response.read()
                    with open(local_path, "wb") as f:
                        f.write(file_data)
            except Exception as e:
                print(f"Failed to download {item['path']}: {e}")

def main():
    if len(sys.argv) < 2:
        print("사용법: python gitdown.py [GitHub_URL]")
        return

    url = sys.argv[1]
    try:
        info = parse_github_url(url)
    except Exception as e:
        print(f"URL 파싱 오류: {e}")
        return

    print(f"--- GitDown CLI (Folder Mode) ---")
    print(f"Target: {info['owner']}/{info['repo']} ({info['branch']})")
    print(f"Path: {info['path']}")
    print(f"Local Dir: {info['name']}")
    print(f"---------------------------------")

    # 시작 폴더 생성
    local_base_dir = info['name']
    if not os.path.exists(local_base_dir):
        os.makedirs(local_base_dir)

    # 원격 경로 자체를 기준으로 상대 경로를 계산하여 중복 폴더 생성을 방지
    remote_base_path = info['path']
    
    download_item(info['owner'], info['repo'], info['path'], info['branch'], local_base_dir, remote_base_path)

    print(f"---------------------------------")
    print(f"완료! '{local_base_dir}' 폴더에 다운로드되었습니다.")

if __name__ == "__main__":
    main()
