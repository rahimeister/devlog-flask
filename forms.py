import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

def password_check(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Şifre en az bir büyük harf içermelidir.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Şifre en az bir rakam içermelidir.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Şifre en az bir özel karakter içermelidir.")

class RegisterForm(FlaskForm):
    name = StringField("Ad Soyad", validators=[DataRequired()])
    email = StringField("E-posta", validators=[DataRequired(), Email()])
    username = StringField("Kullanıcı Adı", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Şifre", validators=[DataRequired(), Length(min=6), password_check])
    confirm = PasswordField("Şifre Tekrar", validators=[DataRequired(), EqualTo("password", message="Şifreler eşleşmiyor.")])

class LoginForm(FlaskForm):
    username = StringField("Kullanıcı Adı", validators=[DataRequired()])
    password = PasswordField("Şifre", validators=[DataRequired()])


class ArticleForm(FlaskForm):
    title = StringField("Başlık", validators=[DataRequired(), Length(min=5, max=300)])
    category = SelectField("Kategori", choices =[
        ('Python', 'Python'), 
        ('JavaScript', 'JavaScript'),
        ("mySQL", "mySQL"),
        ("Bootstrap", "Bootstrap"),
        ("Fronted", "Fronted"),
        ("Backend", "Backend"),
        ("Genel Notlar", "Genel Notlar"),
        ])
    content = TextAreaField("İçerik", validators=[DataRequired()])
