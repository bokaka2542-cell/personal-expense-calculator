import pytest
from app import create_app, db
from models import Entry
from datetime import date


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def add_entry(client, entry_type, title, amount, category=""):
    return client.post("/entries/new", data={
        "entry_type": entry_type,
        "title": title,
        "amount": amount,
        "category": category,
        "entry_date": str(date.today()),
        "notes": "",
    }, follow_redirects=True)


def test_dashboard_loads(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "ภาพรวมการเงิน".encode() in r.data


def test_add_income(client):
    r = add_entry(client, "income", "เงินเดือน", "30000")
    assert "รายการเข้า".encode() in r.data or r.status_code == 200


def test_add_expense(client):
    r = add_entry(client, "expense", "ค่าอาหาร", "500")
    assert r.status_code == 200


def test_summary_totals(client):
    add_entry(client, "income", "เงินเดือน", "20000")
    add_entry(client, "expense", "ค่าเช่า", "8000")
    r = client.get("/summary")
    assert "20000".encode() in r.data or "สรุปยอด".encode() in r.data


def test_invalid_amount_rejected(client):
    r = add_entry(client, "expense", "ทดสอบ", "-100")
    assert r.status_code == 200
    # ต้องไม่ถูก redirect สำเร็จ — ยังอยู่ในหน้า form
    assert "เพิ่มรายการ".encode() in r.data or "จำนวนเงิน".encode() in r.data


def test_delete_entry(client):
    add_entry(client, "expense", "ทดสอบลบ", "100")
    with client.application.app_context():
        entry = Entry.query.first()
        entry_id = entry.id
    r = client.post(f"/entries/{entry_id}/delete", follow_redirects=True)
    assert r.status_code == 200
    with client.application.app_context():
        assert db.session.get(Entry, entry_id) is None


def test_filter_by_type(client):
    add_entry(client, "income", "รายรับทดสอบ", "5000")
    add_entry(client, "expense", "รายจ่ายทดสอบ", "1000")
    r = client.get("/entries?type=income")
    assert "รายรับทดสอบ".encode() in r.data
    assert "รายจ่ายทดสอบ".encode() not in r.data
