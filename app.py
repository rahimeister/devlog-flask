import os 
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_mysqldb import MySQL
from forms import RegisterForm, LoginForm, ArticleForm
from passlib.hash import sha256_crypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config["MYSQL_HOST"] = os.getenv('DB_HOST')
app.config["MYSQL_USER"] = os.getenv('DB_USER')
app.config["MYSQL_PASSWORD"] = os.getenv('DB_PASSWORD')
app.config["MYSQL_DB"] = os.getenv('DB_NAME')
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# ---- Anasayfa ----
@app.route('/')
def index():
    return render_template('index.html')

# ---- Hakkımda ----
@app.route('/about')
def about():
    return render_template('about.html')

# ---- Makaleler ----
@app.route('/articles')
def articles():
    cursor = mysql.connection.cursor()

    keyword = request.args.get('keyword', '')

    if keyword:
        cursor.execute("SELECT * FROM articles WHERE title LIKE %s OR content LIKE %s OR category LIKE %s",
                       ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    else:
        cursor.execute("SELECT * FROM articles")

    articles = cursor.fetchall()
    cursor.close()
    return render_template('articles.html' , articles=articles, keyword=keyword)


@app.route('/article/<string:id>')
def article(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
    article = cursor.fetchone()
    cursor.close()
    return render_template('article.html', article=article)




# ---- Kayıt Olma ----
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.hash(form.password.data)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username,email,password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cursor.close()  
        flash("Kayıt başarılı!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



# ---- login ----
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password_input = form.password.data

        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

        if result > 0:
            user  = cursor.fetchone()
            cursor.close()
            if sha256_crypt.verify(password_input, user["password"]):
                session["logged_in"] = True
                session["username"] = username
                flash("Hoş geldiniz!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Şifre hatalı.", "danger")
        else:
            cursor.close()
            flash("Kullanıcı bulunamadı.", "danger")

    return render_template("login.html", form=form)

# ---- logout ----
@app.route('/logout')
def logout():
    session.clear()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for('index'))

# ----dashboard ----
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM articles WHERE author = %s", (session['username'],))
        articles = cursor.fetchall()
        cursor.close()
        return render_template('dashboard.html', articles=articles)
    else:
        flash("Bu sayfayı görüntülemek için lütfen giriş yapın.", "danger")
        return redirect(url_for('login'))

#----add article ----
@app.route('/addarticle', methods=['GET', 'POST'])
def addarticle():
    if not session.get('logged_in'):
        flash("Bu sayfayı görüntülemek için lütfen giriş yapın.", "danger")
        return redirect(url_for('login'))
    
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        content = form.content.data
        author = session['username']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO articles (title, category, content, author) VALUES (%s, %s, %s, %s)",
                       (title, category, content, author))
        mysql.connection.commit()
        cursor.close()

        flash("Makale başarıyla eklendi!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('addarticle.html', form=form)


#---- edit article ----  

@app.route('/editarticle/<string:id>', methods=['GET', 'POST'])
def editarticle(id):
    if not session.get('logged_in'):
        flash("Bu işlemi gerçekleştirmek için lütfen giriş yapın.", "danger")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = %s AND author = %s", (id, session['username']))
    article = cursor.fetchone()
    cursor.close()

    if not article:
        flash("Makale bulunamadı veya erişim engellenmiş.", "danger")
        return redirect(url_for('dashboard'))
    
    form = ArticleForm()

    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        content = form.content.data

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE articles SET title = %s, category = %s, content = %s WHERE id = %s AND author = %s",
                       (title, category, content, id, session['username']))
        mysql.connection.commit()
        cursor.close()

        flash("Makale başarıyla güncellendi!", "success")
        return redirect(url_for('dashboard'))

     # Formu mevcut verilerle doldur
    form.title.data = article['title']
    form.category.data = article['category']
    form.content.data = article['content']

    return render_template('editarticle.html', form=form, article=article)

#----delete article ----  

@app.route('/deletearticle/<string:id>')
def deletearticle(id):
    if not session.get('logged_in'):
        flash("Bu işlemi gerçekleştirmek için lütfen giriş yapın.", "danger")
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM articles WHERE id = %s AND author = %s", (id, session['username']))
    mysql.connection.commit()
    cursor.close()

    flash("Makale başarıyla silindi!", "success")
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)