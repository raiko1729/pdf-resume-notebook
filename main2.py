from pdf2image import convert_from_bytes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import io
from reportlab.lib.utils import ImageReader

def pdf_with_notes(input_pdf_bytes, output_stream):
    # PDFを画像に変換 (メモリ節約のためDPIを100に)
    images = convert_from_bytes(input_pdf_bytes, dpi=100)

    width, height = A4  # A4サイズ (595 x 842 pt)
    c = canvas.Canvas(output_stream, pagesize=A4)

    # 2ページずつ処理
    for i in range(0, len(images), 2):
        # --- ① 先にA4全面にドットを描画 ---
        spacing = 5 * mm
        radius = 0.3 * mm
        c.setFillGray(0.8)  # 薄いグレー
        y_dot = spacing
        while y_dot < height:
            x_dot = spacing
            while x_dot < width:
                c.circle(x_dot, y_dot, radius, fill=1, stroke=0)
                x_dot += spacing
            y_dot += spacing

        # --- ② 左側のページを配置 ---
        img_left = images[i]
        img_buffer_left = io.BytesIO()
        img_left.save(img_buffer_left, format="PNG")
        img_buffer_left.seek(0)

        target_width = width * 0.5  # 左右に2つ配置するため50%に
        target_height = height * 0.7

        # 左側の配置位置（上詰め）
        x_left = width * 0.00
        y_left = height - target_height - (height * 0.05)

        img_reader_left = ImageReader(img_buffer_left)
        c.drawImage(
            img_reader_left,
            x_left, y_left,
            width=target_width,
            height=target_height,
            preserveAspectRatio=True,
            anchor='nw'
        )

        # --- ③ 右側のページを配置（存在する場合） ---
        if i + 1 < len(images):
            img_right = images[i + 1]
            img_buffer_right = io.BytesIO()
            img_right.save(img_buffer_right, format="PNG")
            img_buffer_right.seek(0)

            # 右側の配置位置（上詰め）
            x_right = width * 0.5 + width * 0.00
            y_right = height - target_height - (height * 0.05)

            img_reader_right = ImageReader(img_buffer_right)
            c.drawImage(
                img_reader_right,
                x_right, y_right,
                width=target_width,
                height=target_height,
                preserveAspectRatio=True,
                anchor='nw'
            )

        c.showPage()

    c.save()


if __name__ == "__main__":
    # テスト用
    with open("resume.pdf", "rb") as f:
        pdf_bytes = f.read()
    with open("output_with_notes.pdf", "wb") as f:
        pdf_with_notes(pdf_bytes, f)