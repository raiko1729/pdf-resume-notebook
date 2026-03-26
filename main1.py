from pdf2image import convert_from_bytes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import io

def pdf_with_notes(input_pdf_bytes, output_stream):
    # PDFを画像に変換 (メモリ上のバイトデータから)
    images = convert_from_bytes(input_pdf_bytes, dpi=150)

    width, height = A4  # A4サイズ (595 x 842 pt)
    c = canvas.Canvas(output_stream, pagesize=A4)

    for i, img in enumerate(images):
        # 画像もメモリ上のバッファに保存
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

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

        # --- ② その上にレジュメ画像を描画（縮小、上詰め中央） ---
        target_width = width * 0.7
        target_height = (height / 2) * 0.7

        x = (width - target_width) / 2
        y = height/2 + (height/2 - target_height)

        from reportlab.lib.utils import ImageReader
        img_reader = ImageReader(img_buffer)

        c.drawImage(
            img_reader,
            x, y,
            width=target_width,
            height=target_height,
            preserveAspectRatio=True,
            anchor='n'
        )

        c.showPage()

    c.save()


if __name__ == "__main__":
    # テスト用
    with open("resume.pdf", "rb") as f:
        pdf_bytes = f.read()
    with open("output_with_notes.pdf", "wb") as f:
        pdf_with_notes(pdf_bytes, f)
