import qrcode
from PIL import Image

# ลิงก์สำหรับเช็คอิน
url = "https://meeting-checkin.onrender.com/check"

# โหลดโลโก้ (ควรใช้ .png พื้นโปร่งใส ขนาดเล็กๆ ประมาณ 100x100 px)
logo_path = "static/logo.png"  # เปลี่ยนชื่อไฟล์ถ้าจำเป็น

# สร้าง QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # สำคัญ: รองรับโลโก้
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# แปลง QR เป็นรูปภาพ
qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# เปิดโลโก้
logo = Image.open(logo_path)

# ปรับขนาดโลโก้
qr_width, qr_height = qr_img.size
logo_size = int(qr_width * 0.25)
logo = logo.resize((logo_size, logo_size))

# คำนวณตำแหน่งโลโก้ (ให้อยู่ตรงกลาง)
pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

# วางโลโก้ลงไปใน QR Code
qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

# บันทึกเป็นไฟล์
qr_img.save("checkin_qr_with_logo.png")

print("✅ สร้าง QR พร้อมโลโก้เสร็จแล้ว: checkin_qr_with_logo.png")
