# GitDown CLI
GitHub 저장소의 특정 폴더를 터미널에서 즉시 다운로드할 수 있는 파이썬 도구입니다.
## 설치 방법 (Linux / macOS)
아래 명령어를 복사하여 터미널에 입력하면 시스템 어디서나 `gitdown` 명령어를 사용할 수 있습니다.
```bash
sudo curl -L https://raw.githubusercontent.com/purndal/gitdown/master/gitdown.py -o /usr/local/bin/gitdown
sudo chmod +x /usr/local/bin/gitdown
```
## 사용 방법
터미널에서 `gitdown` 뒤에 다운로드하고 싶은 GitHub 폴더의 주소를 입력합니다.
gitdown [GitHub 폴더 주소]
### 예시
gitdown https://github.com/ONLYOFFICE/core-fonts/tree/master/droid
## 주요 특징
- 브라우저 없이 터미널에서 즉시 실행 가능합니다.
- ZIP 압축 없이 폴더 구조 그대로 현재 위치에 다운로드합니다.
- 별도의 라이브러리 설치가 필요 없는 순수 파이썬 스크립트입니다.
## 요구 사항
- Python 3.x
