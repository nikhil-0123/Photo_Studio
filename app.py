from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import backgraund
import replacebg
import text_to_image as ti
import enhancement as en

app = Flask(__name__)
app.secret_key = '2007'
app.config['UPLOAD_FOLDER']="static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
currentDirName = os.path.dirname(__file__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with sqlite3.connect('photo_studio.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        print(f"User tuple from the database: {user}")
        if user and len(user) >= 4 and check_password_hash(user[4], password):
            session['username'] = username
            cur = conn.cursor()
            cur.execute("SELECT email,name FROM users WHERE username = ? ",(username,))
            messages = cur.fetchone()
            print(messages)
            f, l = messages[1].split()
            fl = f[0]+l[0]
            fl = fl.upper()
            session['fl']=fl
            session['msg']=messages
            return render_template('home.html',messages=messages,profile=fl)
        else:
            flash('username or password is incorrect try again ! ')
            return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email',None)
    session.pop('name',None)
    session.pop('file',None)
    return redirect(url_for('login'))

@app.route('/register', methods=[ 'GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('ps')
        password_confirm = request.form.get('pscon')

        if len(username) <6:
            flash('Username must be more than 6 charactor !!', 'error')
            return render_template('registration.html')
        if len(password) < 8 :
            flash('password must be more than 8 charactor !!', 'error')
            return render_template('registration.html')
            pass
        if password != password_confirm:
            flash('Password and confirmation do not match', 'error')
            return render_template('registration.html')

        with sqlite3.connect('photo_studio.db', check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            existing_user = cursor.fetchone()
            print(existing_user)
            if existing_user:
                flash('Username or email already exists', 'error')
                return render_template('registration.html')

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO users (username, email, name, password) VALUES (?, ?, ?, ?)", (username, email, name, hashed_password))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('index'))
    return render_template('registration.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pass
    fl=session['fl']
    messages=session['msg']
    return render_template('home.html',messages=messages,profile=fl)
    username = session['username']
    with sqlite3.connect('photo_studio.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?",(username))
        data = cursor.fetchone()
        email = data[2]
        f_name = data[3]
        name.setText(f_name)

@app.route('/basic_editor', methods=['GET', 'POST'])
def basic_editor():
    return render_template('basic_editor.html')

@app.route('/ai_editor', methods=['GET', 'POST'])
def ai_editor():
    if request.method == 'POST':
        pass
    return render_template('ai_editor.html')

@app.route('/editor', methods=['GET','POST'])
def editor():
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return "error no selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        username = session['username']
        conn=sqlite3.connect("photo_studio.db")
        cur=conn.cursor()
        # cur.execute("SELECT image_data FROM user_images WHERE user_id = ?",(username))
        # data = cur.fetchone()
        # if filename in data:
        #     render_template('ai_editor.html',result_img=filename)
        cur.execute("INSERT INTO user_images (user_id, image_data) VALUES(?,?)",(username,file.filename))
        conn.commit()
        session['file'] = filename
        return render_template('ai_editor.html',result_img=filename)

@app.route('/removebg', methods=['GET', 'POST'])
def removebg():
    inputs_dir = os.path.join(currentDirName, 'static/uploads/')
    image_src = session['file']
    image = inputs_dir+image_src
    result = backgraund.removeBackground(image,image_src)
    return render_template('ai_editor.html',result=result)

@app.route('/replacebg', methods=['GET', 'POST'])
def replacebackground():
    inputs_dir = os.path.join(currentDirName, 'static/uploads/')
    image_src = session['file']
    image = inputs_dir+image_src
    file = request.files['input']
    filename = secure_filename(file.filename)
    file.save(os.path.join('static/Result/background/', filename))
    bg='static/Result/background/'+filename
    if file.filename == '':
        flash('No selected file')
        return "error no selected file"
    session['images'] = filename
    result = replacebg.replace(image,bg,image_src)
    return render_template('ai_editor.html',result=result)

@app.route('/bgcolor',methods=['GET','POST'])
def bgcolor():
    color = request.form.get('bg-color')
    if color:
        inputs_dir = os.path.join(currentDirName, 'static/uploads/')
        image_src = session['file']
        image = os.path.join(inputs_dir, image_src)
        result = replacebg.replacecolor(image, color, image_src)
        return render_template('ai_editor.html', result=result)
    else:
        flash('Background color not provided', 'error')
        return redirect(url_for('ai_editor'))
        
@app.route('/text_image',methods=['GET','POST'])
def text_image():
    text = request.form.get('promot')
    print(text)
    result = ti.text2image(text)
    return render_template('ai_editor.html', generated=result)

@app.route('/upscale',methods=['POST','GET'])
def upscale():
    size = request.form['size']
    inputs_dir = os.path.join(currentDirName, 'static/uploads/')
    image_src = session['file']
    image = inputs_dir+image_src
    result = en.inference(image,size,image_src)
    return render_template('ai_editor.html', upscale=result)

if __name__ == '__main__':
    app.run(debug=True)
