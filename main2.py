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
        img_path_left = f"temp_page_{i}.png"
        img_left.save(img_path_left, "PNG")

        target_width = width * 0.5  # 左右に2つ配置するため50%に
        target_height = height * 0.7

        # 左側の配置位置（上詰め）
        x_left = width * 0.00  # 左端から0%のマージン，調節する場合は右側のページの中央からどれだけ右側に配置するかの値も同様に変更する
        y_left = height - target_height - (height * 0.05)  # 上端から5%のマージン

        c.drawImage(
            img_path_left,
            x_left, y_left,
            width=target_width,
            height=target_height,
            preserveAspectRatio=True,
            anchor='nw'
        )
        os.remove(img_path_left)

        # --- ③ 右側のページを配置（存在する場合） ---
        if i + 1 < len(images):
            img_right = images[i + 1]
            img_path_right = f"temp_page_{i+1}.png"
            img_right.save(img_path_right, "PNG")

            # 右側の配置位置（上詰め）
            x_right = width * 0.5 + width * 0.00  # 中央から右側に配置
            y_right = height - target_height - (height * 0.05)

            c.drawImage(
                img_path_right,
                x_right, y_right,
                width=target_width,
                height=target_height,
                preserveAspectRatio=True,
                anchor='nw'
            )
            os.remove(img_path_right)

        c.showPage()

    c.save()


if __name__ == "__main__":
    pdf_with_notes("resume.pdf", "output_with_notes.pdf")