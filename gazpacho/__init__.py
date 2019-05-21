import json, urllib, os, sqlite3

from flask import Flask, render_template, flash, request, session, redirect, url_for

import os
from datetime import datetime
from utils import db
from utils import api
# from utils import api
from random import choice

DIR = os.path.dirname(__file__) or '.'
DIR += '/'

DB_FILE = DIR + 'data/teesk.db'
# print(DB_FILE)

app = Flask(__name__)
user = None
app.secret_key = os.urandom(32)
data = db.DB_Manager(DB_FILE)
# '''
#_choice = ""
#search = ""
# data.createUsers()
# data.createTyping()
# data.createVocab()
# data.createActivities()

def setUser(userName):
    global user
    user = userName

def validateUser():
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('main'))
# '''
@app.route('/', methods=['POST', 'GET'])
def home():
    """Landing page"""
    return render_template('home.html', loggingin = True)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """login users"""
    return render_template('login.html', loggingin = False)

# '''
@app.route('/wanna_register', methods=['POST', 'GET'])
def wanna_register():
    """Registers users"""
    return render_template('register.html', loggingin = False)

@app.route('/auth', methods=['POST'])
def auth():
    """Authentication route. Reroutes to home route when authenticated."""
    # instantiates DB_Manager with path to DB_FILE
    data = db.DB_Manager(DB_FILE)
    # LOGGING IN
    if request.form["action"] == "Login":
        username, password = request.form["username_login"], request.form['password_login']
        if username != "" and password != "" and data.verifyUser(username, password ) :
            session[username] = password
            setUser(username)
            data.save()
            return redirect(url_for('main'))
        # user was found in DB but password did not match
        elif data.findUser(username):
            flash('Incorrect password!')
        # user not found in DB at all
        else:
            flash('Incorrect username!')
        data.save()
        return redirect(url_for("login"))

@app.route('/create_account_action', methods=["POST"])
def create_account_action():
    """Creates account. Reroutes to home when successful."""
    data = db.DB_Manager(DB_FILE)
    username, password, password2 = request.form["username_reg"], request.form['password_reg'], request.form['password_check']
    bad_string = '!@#$%^&*() {|\\}[]?><,./;\'\"=+-_'
    for char in bad_string:
        if username.find(char) != -1:
            flash('Please input a valid username!')
            return redirect(url_for("wanna_register"))

    if len(username.strip()) != 0 and not data.findUser(username):
        if len(password.strip()) != 0:
            # add the account to DB
            if password != password2:
                flash('Passwords must match')
            else:
                data.registerUser(username, password)
                data.save()
                flash('Created account')
                return redirect(url_for('home'))
        else:
            flash('Password needs to have stuff in it')
    elif len(username) == 0:
        flash("Username needs to have stuff in it")
    else:
        flash("Username already taken!")
    # TRY TO REGISTER AGAIN
    return render_template("home.html")

@app.route('/logout')
def logout():
    """Logs the user out"""
    validateUser()
    session.pop(user, None)
    setUser(None)
    return redirect(url_for('home'))

@app.route('/tracker')
def tracker():
    """Tracks calories."""
    validateUser()


@app.route('/main', methods=['POST', 'GET'])
def main():
    """Activities page."""
    if user in session:
        data = db.DB_Manager(DB_FILE)

        token=request.args.get('token')
        user_id= request.args.get('user_id')
        '''
        [add code if user doesnt have token/id, display authorization option]
        '''
        #api.setUserId(user_id)
        #api.setAccessToken(token)
        # print("token: "+str(request.args.get('token')))
        # print("user_id: "+str(request.args.get('user_id')))
        if token != None and user_id != None:
            api.setUserId(str(user_id))
            api.setAccessToken(str(token))
            api.setHeaders(str(token))
            profile= api.fetchProfile(str(user_id))
        else:
            profile= "woah" 

        return render_template("home.html",profile=profile)
    profile= "empty"
    return render_template("home.html", loggingin = True, profile= profile)

if __name__ == "__main__":
    app.debug = True
    app.run()
