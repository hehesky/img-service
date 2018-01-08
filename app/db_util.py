##using python 2 syntax (print and others)
#By Kaihua Zhou 
#2017-10

import mysql.connector
from config import *
"""Please put databases related info in config.py
required info:

HOSTNAME : host of your MySQL server
DB_USERNAME : username for database
DB_PASSWORD : password
DB_NAME : name of database to use

 """

create_user_table = \
r"CREATE TABLE IF NOT EXISTS users ( username VARCHAR(20) Primary Key, salt VARCHAR(100) NOT NULL, password VARCHAR(100) Not NULL) engine=INNODB;"

create_img_table = \
'create table if not exists images(image_id Varchar(40) primary key not null, user VARCHAR(20), upload_time timestamp default current_timestamp, foreign key(user) references users(username) on delete cascade)engine=INNODB;'
insert_user_template = r'INSERT INTO users(username,salt,password) values(%s,%s,%s);'
query_user_template = r'SELECT * from users WHERE username = %s;'

insert_img_template = r'INSERT INTO images(image_id,user) values(%s,%s);'
query_image_template = r'SELECT * from images WHERE user = %s;'




def create_conn():
    try:
        conn=mysql.connector.connect(host=HOSTNAME,user=DB_USERNAME,passwd=DB_PASSWORD,db=DB_NAME)
        return conn
    except mysql.connector.Error as e:
        print str(e)
        return None

def exec_query(conn,query,args,fetch=True):
    """execute a SQL query and return all matched rows"""
    if conn.is_connected() is False:
        conn=create_conn()

    cur=conn.cursor(buffered=True)
    cur.execute(query,args)
    conn.commit()
    if fetch is True:
        result=cur.fetchall()
        return result

#password is already salted
def add_new_user(conn,username,salt,password):
    args=(username,salt,password)
    try:
        exec_query(conn,insert_user_template,args,False)
        return True
    except mysql.connector.Error as e:
        print e
        return e  

def query_user(conn,username):
    args=(username,)
    try:
        ret=exec_query(conn,query_user_template,args)
        return ret
    except mysql.connector.Error as e:
        print e
        return None

#image_id shall include file format (.jpg, .png, etc...)
def add_image(conn,image_id,username):
    args=(image_id,username)
    try:
        exec_query(conn,insert_img_template,args,False)
        return True
    except mysql.connector.Error as error:
        print error
        return error

def query_image(conn,username):
    args=(username,)
    try:
        ret=exec_query(conn,query_image_template,args)
        return ret
    except mysql.connector.Error as e:
        print e
        return None



def init_database():
    """initialize database, create users table(more tables to be added)"""

    print "INFO: initializing database"
    conn=create_conn()
    if conn is None:
        raise Exception("Cannot connect to database.")
    try:
        cur=conn.cursor(buffered=True)
        cur.execute(create_user_table)
        conn.commit()
        print "created users table"
        cur.execute(create_img_table)
        conn.commit()
        print "created imgaes table"
        print "returning conn object"
        return conn
    except mysql.connector.Error as e:
        print e
    


