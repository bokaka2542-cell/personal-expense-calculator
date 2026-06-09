# แอปบัญชีรายรับรายจ่ายส่วนตัว

เว็บแอปภาษาไทยสำหรับบันทึกและคำนวณค่าใช้จ่ายส่วนตัว พัฒนาด้วย Python Flask พร้อมนำขึ้น GitHub และ Deploy บน Render ได้

## ความสามารถ

- เพิ่ม `รายการเข้า` เช่น เงินเดือน รายได้พิเศษ
- เพิ่ม `รายการออก` เช่น ค่าอาหาร ค่าเดินทาง ค่าเช่า
- แสดง `สรุปยอด` รายรับรวม รายจ่ายรวม และยอดคงเหลือ
- ดูรายการทั้งหมดและกรองตามประเภท
- แก้ไขและลบรายการ
- สรุปยอดตามเดือนและหมวดหมู่
- ใช้ SQLite ตอนรันในเครื่อง และ PostgreSQL ตอน Deploy บน Render

## โครงสร้างโปรเจกต์

```text
app.py
config.py
models.py
forms.py
routes.py
templates/
static/
tests/
requirements.txt
Procfile
render.yaml
```

## วิธีรันในเครื่อง

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

เปิดเว็บที่:

```text
http://127.0.0.1:5000
```

## วิธีทดสอบ

```bash
pytest
```

## การตั้งค่าสภาพแวดล้อม

คัดลอกไฟล์ `.env.example` เป็น `.env` แล้วแก้ค่าได้ตามต้องการ

```text
SECRET_KEY=change-me-in-production
DATABASE_URL=
FLASK_DEBUG=1
```

ถ้าไม่กำหนด `DATABASE_URL` ระบบจะใช้ SQLite ที่ `instance/expenses.db`

## Deploy บน Render

โปรเจกต์นี้มีไฟล์ `render.yaml` และ `Procfile` พร้อมใช้งาน

### วิธีที่แนะนำ

1. Push โปรเจกต์ขึ้น GitHub
2. เข้า Render แล้วเลือก New Blueprint
3. เลือก Repository นี้
4. Render จะสร้าง Web Service และ PostgreSQL ให้ตาม `render.yaml`
5. เปิด URL ที่ Render สร้างให้

### คำสั่ง Build / Start

Build Command:

```text
pip install -r requirements.txt
```

Start Command:

```text
gunicorn app:app
```

## หมายเหตุ

อย่า Commit ไฟล์เหล่านี้ขึ้น GitHub:

- `.env`
- `.venv/`
- `instance/`
- ฐานข้อมูล SQLite ในเครื่อง
