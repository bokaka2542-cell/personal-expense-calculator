from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import func, extract
from datetime import date
from app import db
from models import Entry
from forms import EntryForm

bp = Blueprint("main", __name__)


def get_totals(query=None):
    q = query or Entry.query
    income = db.session.query(func.sum(Entry.amount)).filter(Entry.entry_type == "income").scalar() or 0
    expense = db.session.query(func.sum(Entry.amount)).filter(Entry.entry_type == "expense").scalar() or 0
    return float(income), float(expense), float(income) - float(expense)


@bp.route("/")
def index():
    income, expense, balance = get_totals()
    recent = Entry.query.order_by(Entry.entry_date.desc(), Entry.created_at.desc()).limit(10).all()
    return render_template("index.html", income=income, expense=expense, balance=balance, recent=recent)


@bp.route("/entries")
def entries():
    filter_type = request.args.get("type", "")
    q = Entry.query
    if filter_type in ("income", "expense"):
        q = q.filter_by(entry_type=filter_type)
    all_entries = q.order_by(Entry.entry_date.desc(), Entry.created_at.desc()).all()
    return render_template("entries.html", entries=all_entries, filter_type=filter_type)


@bp.route("/entries/new", methods=["GET", "POST"])
def new_entry():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(
            entry_type=form.entry_type.data,
            title=form.title.data,
            amount=form.amount.data,
            category=form.category.data,
            entry_date=form.entry_date.data,
            notes=form.notes.data,
        )
        db.session.add(entry)
        db.session.commit()
        label = "รายการเข้า" if entry.entry_type == "income" else "รายการออก"
        flash(f"เพิ่ม{label}สำเร็จ", "success")
        return redirect(url_for("main.index"))
    return render_template("entry_form.html", form=form, title="เพิ่มรายการ")


@bp.route("/entries/<int:entry_id>/edit", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = db.get_or_404(Entry, entry_id)
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        flash("แก้ไขรายการสำเร็จ", "success")
        return redirect(url_for("main.entries"))
    return render_template("entry_form.html", form=form, title="แก้ไขรายการ")


@bp.route("/entries/<int:entry_id>/delete", methods=["POST"])
def delete_entry(entry_id):
    entry = db.get_or_404(Entry, entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("ลบรายการสำเร็จ", "info")
    return redirect(url_for("main.entries"))


@bp.route("/summary")
def summary():
    income, expense, balance = get_totals()

    monthly = db.session.query(
        extract("year", Entry.entry_date).label("year"),
        extract("month", Entry.entry_date).label("month"),
        Entry.entry_type,
        func.sum(Entry.amount).label("total"),
    ).group_by("year", "month", Entry.entry_type).order_by("year", "month").all()

    categories = db.session.query(
        Entry.category,
        Entry.entry_type,
        func.sum(Entry.amount).label("total"),
    ).group_by(Entry.category, Entry.entry_type).order_by(Entry.entry_type, Entry.category).all()

    return render_template(
        "summary.html",
        income=income, expense=expense, balance=balance,
        monthly=monthly, categories=categories,
    )
