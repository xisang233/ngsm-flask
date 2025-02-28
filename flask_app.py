# coding:utf-8

from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import time
import shutil
import os

app = Flask(__name__)

basepath = os.getcwd()  # flaskのフォルダ

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # 現在の時間を控え、temp/ でフォルダを新規作成し、アップロード先として設定
        t = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
        workpath = os.path.join(basepath, "temp/%s" %t)
        os.mkdir(workpath)

        # 最小と最多の字数
        a = request.form["from"]
        b = request.form["to"]

        try:
            assert int(a) > 0
        except:
            return "最短字数は、正整数を入力してください。"

        try:
            assert int(b) > 0
            assert int(b) >= int(a)
        except:
            return "最長字数は、最短字数よりも大きい正整数を入力してください。"

        # ファイルを処理する。複数のファイルの処理が可能。セキュリティ上、txtのみ処理する
        # txtファイルは、/temp/時間 に保存。ファイルをここで保存する。1秒以内で複数のリクエストがない限り、リクエストごとのファイルをうまく仕分けることができる

        files = ""
        for file in request.files.getlist("file"):
            filename = file.filename
            if filename.rsplit('.', 1)[1] == "txt":
                print(filename)
                upload_path = os.path.join(workpath, filename)
                file.save(upload_path)
                files += filename + " "

        os.chdir(workpath)
        result = str(os.popen("perl %s/ngsm.pl -g%s,%s %s" %(basepath, a, b, files), "r").read())
        os.chdir(basepath)
        print(result)
        shutil.rmtree(workpath)
        return """<textarea rows="30" cols="100">%s
                </textarea>""" %result
        #return str(result).replace("\n", "</br>").replace("\t", "&nbsp"*10)
    else:
        return "ERROR"

if __name__ == '__main__':
    # 開発用。サーバ環境ではrun.shを実行してください!!
    app.run(debug=True)