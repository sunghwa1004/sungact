from flask import Flask, render_template, request, redirect, url_for
from github import Github
import os

app = Flask(__name__)

# GitHub 저장소 정보
github_token = os.environ.get('MY_GITHUB_TOKEN')
repo_name = 'sunghwa1004/save'
file_name = 'memo.txt'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        memo_content = request.form['memo']
        update_memo(memo_content)
        return redirect(url_for('index'))
    else:
        memo_content = get_memo_content()
        return render_template('index.html', memo=memo_content)

def update_memo(content):
    # GitHub 저장소에 접근하여 메모 업데이트
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    file = repo.get_contents(file_name)
    repo.update_file(file.path, "Update memo", content, file.sha)

def get_memo_content():
    # GitHub 저장소에서 메모 내용 가져오기
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    file = repo.get_contents(file_name)
    decoded_content = file.decoded_content.decode('utf-8')
    return decoded_content

if __name__ == '__main__':
    app.run(debug=True)
