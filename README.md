# DevLog - Flask Kişisel Öğrenme Günlüğü Platformu

## Proje Hakkında

DevLog, yazılım öğrenme sürecinde edinilen bilgilerin düzenli bir şekilde kaydedilmesini sağlayan kişisel öğrenme günlüğü platformudur.

Bu proje ile kullanıcılar:

- Öğrendikleri konular hakkında notlar alabilir
- Kendi yazılarını yönetebilir (ekle, sil, güncelle)
- Yazılar arasında arama yapabilir
- Gelişim süreçlerini takip edebilir

Proje, Python Flask kullanılarak geliştirilmiş olup, kullanıcı yönetimi ve içerik yönetimi özellikleri içermektedir.


## Özellikler
- Kullanıcı kayıt sistemi

- Kullanıcı giriş sistemi

- Session tabanlı yetkilendirme

- Decorator ile sayfa koruma

- Kullanıcıya özel kontrol paneli

- Yazı ekleme (CRUD - Create)

- Yazı güncelleme (Update)

- Yazı silme (Delete)

- Yazı listeleme (Read)

- Yazı detay sayfası

- Yazı arama özelliği

- CKEditor ile gelişmiş içerik girişi

- Bootstrap ile responsive (mobil uyumlu) arayüz

- Flash mesaj sistemi

- MySQL veritabanı entegrasyonu


## Kullanılan Teknolojiler
- Python
- Flask
- MySQL
- Jinja2 Template Engine
- Bootstrap
- WTForms
- CKEditor
- XAMPP

---

## Veritabanı Yapısı

### users tablosu

| Alan | Açıklama |
|------|--------|
| id | Kullanıcı ID |
| name | Ad Soyad |
| email | E-posta |
| username | Kullanıcı adı |
| password | Şifre |

---

### articles tablosu

| Alan | Açıklama |
|------|--------|
| id | Yazı ID |
| title | Başlık |
| author | Yazar |
| category | Kategori |
| content | İçerik |
| created_date | Oluşturulma tarihi |

---

## Sayfa Yapısı

- Ana Sayfa  
- Hakkımda  
- Kayıt Ol  
- Giriş Yap  
- Kontrol Paneli  
- Yeni Yazı Ekle  
- Yazılar  
- Yazı Detay  
- Yazı Güncelle  

---

## Kurulum

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/rahimeister/devlog-flask.git
cd devlog 
```

### 2. Sanal Ortam Oluşturun

```bash
python -m venv venv
venv\Scripts\activate
```

### 3.Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```


### 4. Veritabanını Oluşturun

```sql
CREATE DATABASE devlog;
```
### Database Setup

Import the SQL file located in:

```text
database/devlog.sql
```
using phpMyAdmin or MySQL CLI.

### 5. Tabloları Oluşturun 

users
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(50),
    password VARCHAR(255)
);
```

articles
```sql
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(50),
    category VARCHAR(50),
    content TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Uygulamayı Çalıştırın

```bash
python app.py
```

### 7. Tarayıcıda Açın

```text
http://127.0.0.1:5000
```

---

## Geliştirici

Bu proje Flask öğrenme sürecini geliştirmek ve portföy projesi oluşturmak amacıyla geliştirilmiştir.