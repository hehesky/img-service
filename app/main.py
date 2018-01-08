# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 18:38:34 2017

@author: Kaihua
"""


import os
import signal
import sys
from flask import Flask, session, render_template, request, g, url_for
import flask
import login
import db_util
import os
import os.path
import uuid
from werkzeug import secure_filename
from wand_util import process_img
import json
from ConnHolder import ConnHolder
import boto3
from app import app
from config import *
#[Region]before app launches

"""Important: set your S3 access info as environment variables
Check config.py file before starting

"""


s3 = boto3.client('s3',aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET) 
#S3 Client used for upload images to S3 bucket

connHolder=ConnHolder()

def keyboad_interrupt_handler(signal,frame):
    
    if connHolder.conn != None and connHolder.conn.is_connected():
        connHolder.close()
    sys.exit()

signal.signal(signal.SIGINT,keyboad_interrupt_handler)


###[Region]routing logics
@app.route('/',)
def index():
    #if g.user exists, which means the user is logged in previously, render dashboard directly
    if g.user:
        return flask.redirect('/dashboard')
        
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def user_login():
    """render login page in GET method. Verify username and password in POST mode"""
    session.pop('user',None)

    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form['username']
        password=request.form['password']

        if login.verify_password(connHolder.conn,username,password) is True:
            session['user']=username
            
            return flask.redirect('/dashboard')
        else:
            
            return flask.redirect(url_for('.custom', message="login failed", type="login"))

@app.route("/register",methods=['GET','POST'])
def register():
    #To be improved    
    session.pop('user',None)
    if request.method=='GET':
        return render_template('register.html')
    else:
        username=request.form['username']
        password=request.form['password']
        state=login.register(connHolder.conn,username,password)
        if state is True: #state is either 'True' or a string with error message
            session['user']=username
            return flask.redirect('/dashboard')
        else:
            return flask.redirect(url_for('.custom', message="Error: "+ str(state), type="register"))


@app.route('/dashboard')
def show_dashboard():
    if g.user is None:
        return flask.redirect('/')
    else:
        pictures = login.retrieve_pic(connHolder.conn,session['user'])

    return render_template('dashboard.html',username=session['user'], pic = json.dumps(pictures))


    
@app.before_request
def session_check():
    g.user=None
    if 'user' in session:
        g.user=session['user']

@app.route('/logout')
def logout():
    session.pop('user',None)
    return flask.redirect("/")

@app.route('/custom')
def custom():
    return render_template('custom.html', message = request.args.get('message'), type = request.args.get('type'))

@app.route('/upload',methods=['GET','POST'])
def upload():
    if g.user is None:
        return flask.redirect('/')
    
    if request.method=='GET':
        return render_template('upload.html')
    else:
        username=g.user
        f=request.files['imgfile']
        #cache path is <approot>/cache
        if os.path.isdir('cache') is False:
            os.mkdir('cache')
        cache_dir="cache"

        filename=secure_filename(f.filename)
        
        ext=os.path.splitext(filename)[1] #get extension name of file
        
        img_id=str(uuid.uuid4())
        save_filename=img_id+ext#name of saved file(the original), e.g. <uuid>.jpg
        save_path=os.path.join(cache_dir,save_filename)#path to saved original file
        
        f.save(save_path)
        db_util.add_image(connHolder.conn,save_filename,username)
        
        process_img(save_filename,'cache',username)
        redshift_path=os.path.join(cache_dir,"redshift_"+save_filename)
        thumbnail_path=os.path.join(cache_dir,"thumbnail_"+save_filename)
        scifi_path=os.path.join(cache_dir,"scifi_"+save_filename)
        grey_path=os.path.join(cache_dir,"grey_"+save_filename)

        s3.upload_file(save_path,bucketname,save_filename)
        s3.upload_file(redshift_path,bucketname,"redshift_"+save_filename)
        s3.upload_file(thumbnail_path,bucketname,"thumbnail_"+save_filename)
        s3.upload_file(scifi_path,bucketname,"scifi_"+save_filename)
        s3.upload_file(grey_path,bucketname,"grey_"+save_filename)
        return flask.redirect(url_for('.custom', message="Uploaded!", type="upload"))

@app.route('/test/FileUpload',methods=['GET','POST'])
def test_upload():
	session.pop('user',None)
	if request.method=="GET":
		return render_template('test.html')
	else:
		username=request.form['userID']
        password=request.form['password']
        if login.verify_password(connHolder.conn,username,password) is True:
            session['user']=username
            f=request.files['uploadedfile']
            if os.path.isdir('cache') is False:
                os.mkdir('cache')
            cache_dir="cache"

            filename=secure_filename(f.filename)
            
            ext=os.path.splitext(filename)[1] #get extension name of file
            
            img_id=str(uuid.uuid4())
            save_filename=img_id+ext#name of saved file(the original), e.g. <uuid>.jpg
            save_path=os.path.join(cache_dir,save_filename)#path to saved original file
            
            f.save(save_path)
            db_util.add_image(connHolder.conn,save_filename,username)
            
            process_img(save_filename,'cache',username)
            redshift_path=os.path.join(cache_dir,"redshift_"+save_filename)
            thumbnail_path=os.path.join(cache_dir,"thumbnail_"+save_filename)
            scifi_path=os.path.join(cache_dir,"scifi_"+save_filename)
            grey_path=os.path.join(cache_dir,"grey_"+save_filename)

            s3.upload_file(save_path,bucketname,save_filename)
            s3.upload_file(redshift_path,bucketname,"redshift_"+save_filename)
            s3.upload_file(thumbnail_path,bucketname,"thumbnail_"+save_filename)
            s3.upload_file(scifi_path,bucketname,"scifi_"+save_filename)
            s3.upload_file(grey_path,bucketname,"grey_"+save_filename)
            return flask.redirect(url_for('.custom', message="Uploaded!", type="upload"))
        else:
            print "login failed"
            return flask.redirect(url_for('.custom', message="login failed", type="login"))
@app.before_first_request
def init():
    connHolder.set_conn(db_util.init_database())


if __name__=="__main__":
    
    app.run(debug=True)
