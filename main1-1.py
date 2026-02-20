from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import os

def pdf_with_notes(input_pdf, output_pdf):
    # PDFを画像に変換
    images = convert_from_path(input_pdf, dpi=150)

    width, height = A4  # A4サイズ (595 x 842 pt)
    c = canvas.Canvas(output_pdf, pagesize=A4)

    for i, img in enumerate(images):
        img_path = f"temp_page_{i}.png"
        img.save(img_path, "PNG")

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

        c.drawImage(
            img_path,
            x, y,
            width=target_width,
            height=target_height,
            preserveAspectRatio=True,
            anchor='n'
        )

        c.showPage()
        os.remove(img_path)

    c.save()


if __name__ == "__main__":
    pdf_with_notes("resume.pdf", "output_with_notes.pdf")
