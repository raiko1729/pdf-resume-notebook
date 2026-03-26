from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from main1 import pdf_with_notes as pdf_with_notes_1
from main2 import pdf_with_notes as pdf_with_notes_2
import tempfile

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理用

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# フォルダ作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ファイルチェック
        if 'file' not in request.files:
            flash('ファイルが選択されていません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルが選択されていません')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('PDFファイルのみアップロード可能です')
            return redirect(request.url)

        # 処理タイプ取得
        process_type = request.form.get('process_type')
        if process_type not in ['1', '2']:
            flash('処理タイプを選択してください')
            return redirect(request.url)

        # ファイル保存
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # 出力ファイル名 (元のファイル名をベースにする)
        base_filename = os.path.splitext(filename)[0]
        output_filename = f"{base_filename}_with_notes_{process_type}.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # 処理実行
        try:
            if process_type == '1':
                pdf_with_notes_1(input_path, output_path)
            else:
                pdf_with_notes_2(input_path, output_path)
        except Exception as e:
            flash(f'処理中にエラーが発生しました: {str(e)}')
            return redirect(request.url)

        # ダウンロード
        response = send_file(output_path, as_attachment=True, download_name=output_filename)
        response.set_cookie('fileDownload', 'true', path='/')
        return response

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)