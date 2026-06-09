from datetime import date
from app import db


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    entry_type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    category = db.Column(db.String(100), default="")
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
