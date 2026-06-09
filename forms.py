from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from datetime import date


class EntryForm(FlaskForm):
    entry_type = SelectField(
        "ประเภท",
        choices=[("income", "รายการเข้า"), ("expense", "รายการออก")],
        validators=[DataRequired()]
    )
    title = StringField("รายการ", validators=[DataRequired(message="กรุณากรอกรายการ")])
    amount = DecimalField(
        "จำนวนเงิน (บาท)",
        validators=[DataRequired(), NumberRange(min=0.01, message="จำนวนเงินต้องมากกว่า 0")],
        places=2
    )
    category = StringField("หมวดหมู่")
    entry_date = DateField("วันที่", default=date.today)
    notes = TextAreaField("หมายเหตุ")
