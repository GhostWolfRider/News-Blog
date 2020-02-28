import os
from flask import Flask, request, flash, url_for, redirect, render_template,session,escape,send_file,make_response
from flask_sqlalchemy import SQLAlchemy
from tkinter import *
from PIL import ImageTk,Image
from datetime import datetime
import pdfkit


app = Flask(__name__)
app.secret_key='any'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

db = SQLAlchemy(app)

class tb_login1(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   username = db.Column(db.String(100))
   password = db.Column(db.String(50))
   city = db.Column(db.String(50))

class tb_Admin1(db.Model):
   id = db.Column('admin_id', db.Integer, primary_key = True)
   username = db.Column(db.String(100))
   password = db.Column(db.String(50))

class tb_uploads(db.Model):
    id=db.Column('image_id',db.Integer,primary_key = True)
    imagename=db.Column(db.String(200))
    valid=db.Column(db.String(10))
    city=db.Column(db.String(50))

class tb_uploads1(db.Model):
    id=db.Column('image_id',db.Integer,primary_key = True)
    imagename=db.Column(db.String(200))
    valid=db.Column(db.String(10))
    city=db.Column(db.String(50))
    date=db.Column(db.String(50))
    caption=db.Column(db.String(100))
    content=db.Column(db.String(500))

class tb_uploads2(db.Model):
    id=db.Column('image_id',db.Integer,primary_key = True)
    imagename=db.Column(db.String(200))
    valid=db.Column(db.String(10))
    city=db.Column(db.String(50))
    date=db.Column(db.String(50))
    caption=db.Column(db.String(100))
    content=db.Column(db.String(500))
    category=db.Column(db.String(50))

class tb_uploads3(db.Model):
    id=db.Column('image_id',db.Integer,primary_key = True)
    imagename=db.Column(db.String(200))
    Caption=db.Column(db.String(50))
    Content=db.Column(db.String(450))
    Category=db.Column(db.String(10))
    DateTime=db.Column(db.DateTime())
    city=db.Column(db.String(10))
    Uploadedby=db.Column(db.String(10))
    valid=db.Column(db.String(10))

class tb_temp1(db.Model):
    id=db.Column('timage_id',db.Integer,primary_key=True)

class tb_temp2(db.Model):
    pid=db.Column('timage_id',db.Integer,primary_key=True)
    id=db.Column(db.Integer)

def __init__(self,username,password,city):
   self.username = username
   self.password = password
   self.city = city

#UPLOAD_FOLDER = '/home/krunal/projects/news/FlaskWebProject1/uploads'
UPLOAD_FOLDER='/home/krunal/projects/news/FlaskWebProject1/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods = ['GET', 'POST'])
def Login():
    if request.method == 'POST':
        t=tb_temp2.query.all()
        for y in t: 
            session['tid']=y.id
        s=tb_login1.query.all()
        for x in s:
            
            if request.form["uname"]==x.username and request.form["pword"]==x.password:
                session['susername']=x.username
                session['scity']=x.city
                session['sid']=x.id
                return redirect(url_for('home',susername=session['susername'],scity=session['scity']))
            elif request.form["uname"]=='user' and request.form["pword"]=='user':
                return redirect(url_for('show_all'))
            
        return redirect(url_for('Login') )
    else:
        #return redirect(url_for('Login'))
        return render_template('Login.html' )
      

@app.route('/home', methods = ['GET', 'POST'])
def home():
     if session['susername']=='z':
         #return redirect(url_for('Login'))
        return render_template('Login.html')

     else:
        return render_template('home.html',tb_login1 = tb_login1.query.all(),tb_uploads3=tb_uploads3.query.all())

@app.route('/Sports', methods = ['GET', 'POST'])
def Sports():
        return render_template('sports.html',tb_login1 = tb_login1.query.all(),tb_uploads3=tb_uploads3.query.all())

@app.route('/educational', methods = ['GET', 'POST'])
def educational():
        return render_template('educational.html',tb_login1 = tb_login1.query.all(),tb_uploads3=tb_uploads3.query.all())

@app.route('/business', methods = ['GET', 'POST'])
def business():
        return render_template('business.html',tb_login1 = tb_login1.query.all(),tb_uploads3=tb_uploads3.query.all())

@app.route('/lifestyle', methods = ['GET', 'POST'])
def lifestyle():
        return render_template('lifestyle.html',tb_login1 = tb_login1.query.all(),tb_uploads3=tb_uploads3.query.all())

@app.route('/entertainment', methods = ['GET', 'POST'])
def entertainment():
        return render_template('entertainment.html',tb_login1 = tb_login1.query.all(),tb_uploads3=tb_uploads3.query.all())

@app.route('/technology', methods = ['GET', 'POST'])
def technology():
        return render_template('technology.html',tb_login1 = tb_login1.query.all(),tb_uploads3=tb_uploads3.query.all())

@app.route('/show_all', methods = ['GET', 'POST'])
def show_all():
   return render_template('show_all.html', tb_login1 = tb_login1.query.all(),tb_uploads3 = tb_uploads3.query.all() )  

@app.route('/approve_news/<imagepath>', methods = ['GET', 'POST'])
def approve_news(imagepath):
         s=tb_uploads3.query.all()
         for x in s:
              if imagepath==x.imagename:
                  x.valid='yes'
         
         db.session.commit()
         return render_template('show_all.html', tb_login1 = tb_login1.query.all(),tb_uploads3 = tb_uploads3.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['username'] or not request.form['password']:
         flash('Please enter all the fields', 'error')
      else:
         s=tb_login1.query.all()
         for x in s:
              if request.form['username']==x.username:
                  flash('username is already taken please try another one','error')
                  return render_template('new.html')
              
      if  request.form['password']!=request.form['psw-repeat']:
            flash('Password is not matching','error')
            return render_template('new.html')
              
      else:
         tb_log = tb_login1(username=request.form['username'], password=request.form['password'], city=request.form['city'])
         
         db.session.add(tb_log)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

@app.route('/upload_news', methods = ['GET', 'POST'])
def upload_news():
    return render_template('upload_news.html')

@app.route('/uploader', methods=['GET','POST'])
def upload_file():
     if request.method == 'POST':
        file =request.files['file']
        f = os.path.join(file.filename)
        print (os.path.join(file.filename))
        f = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],str(session['tid'])+session['susername']+file.filename))
        tb_up = tb_uploads3(imagename=str(session['tid'])+session['susername']+file.filename,Caption=request.form['caption'],
                            Content=request.form['content'],Category=request.form['category'],DateTime=datetime.now(),
                            city=session['scity'],Uploadedby=session['susername'],valid='no')
        
        q=tb_temp2(id=session['tid']+1)
        db.session.add(q)
        db.session.add(tb_up)
        db.session.commit()
        session['tid']=session['tid']+1
        flash('Record was successfully added')
        return redirect(url_for('home',susername=session['susername'],scity=session['scity']))

@app.route('/update_profile', methods = ['GET', 'POST'])
def update_profile():
   if request.method == 'POST':
      if not request.form['username'] or not request.form['password']:
         flash('Please enter all the fields', 'error')
      else:
           s=tb_login1.query.all()
           for x in s:
                if request.form["username"]==x.username:
                     x.city=request.form['city']
                     x.password=request.form['password']
                     db.session.commit()
                     flash('Record was successfully added')
                     return redirect(url_for('show_all'))
         
                #else:
                     #return render_template("update_profile.html")
        
   return render_template('update_profile.html')

@app.route('/view_image/<imagepath>',methods = ['GET', 'POST'])
def view_image(imagepath):
    
    #print("<html><body><input type='button' text='back' onclick='home.html'></body></html>")
    #return send_file('/home/krunal/projects/news/FlaskWebProject1/uploads'+imagepath, attachment_filename=imagepath)
    return send_file('/home/krunal/projects/news/FlaskWebProject1/uploads/'+imagepath,attachment_filename=imagepath)  
   
@app.route('/Logout')
def Logout():
   #session.clear()
   session['susername']='z'
   #return render_template('Login.html')
   return redirect(url_for('Login'))

@app.route('/Save/<imagepath>',methods = ['GET', 'POST'])
def Save(imagepath):
    rendered=render_template('save.html',imagepath=imagepath,tb_uploads3=tb_uploads3.query.all())
    #rendered = render_template('downloads.html')
    pdf=pdfkit.from_string(rendered,False,configuration=config)
    
    response = make_response(pdf)
    response.headers['Content-Type']= 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=news.pdf'
    return response


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)