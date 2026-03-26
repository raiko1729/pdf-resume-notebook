from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import os
import io
from werkzeug.utils import secure_filename
from main1 import pdf_with_notes as pdf_with_notes_1
from main2 import pdf_with_notes as pdf_with_notes_2

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

ALLOWED_EXTENSIONS = {'pdf'}

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

        # 元のファイル名を安全にする
        filename = secure_filename(file.filename)
        base_filename = os.path.splitext(filename)[0]
        output_filename = f"{base_filename}_with_notes_{process_type}.pdf"

        # メモリ上で処理
        try:
            input_pdf_bytes = file.read()
            output_buffer = io.BytesIO()

            if process_type == '1':
                pdf_with_notes_1(input_pdf_bytes, output_buffer)
            else:
                pdf_with_notes_2(input_pdf_bytes, output_buffer)

            output_buffer.seek(0)
        except Exception as e:
            flash(f'処理中にエラーが発生しました: {str(e)}')
            return redirect(request.url)

        # ダウンロード（メモリから直接送信）
        response = send_file(
            output_buffer,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
        response.set_cookie('fileDownload', 'true', path='/')
        return response

    return render_template('index.html')

if __name__ == "__main__":
    # RenderやGCPが指定するポートを優先。なければデフォルトで 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)