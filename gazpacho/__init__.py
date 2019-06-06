import json, urllib, os, sqlite3

from flask import Flask, render_template, flash, request, session, redirect, url_for, jsonify
from pandas.io.json import json_normalize
import pandas as pd

import os
from datetime import datetime
from utils import db
from utils import api
from utils import food as f
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

userSynced= False #is user synced to Fitbit?
meals= 0 #necessary lol

def setUser(userName):
    global user
    user = userName

def setSynced(bool):
    global userSynced
    userSynced= bool

# '''
@app.route('/', methods=['POST', 'GET'])
def home():
    """Landing page"""
    if user in session:
        print(userSynced)
        return redirect(url_for('main'))
    else:
        return render_template('home.html', loggedIn = False)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """login users"""
    return render_template('login.html', loggedIn = False)

# '''
@app.route('/wanna_register', methods=['POST', 'GET'])
def wanna_register():
    """Registers users"""
    return render_template('register.html', loggedIn = False)

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
                return redirect(url_for("wanna_register"))
            else:
                data.registerUser(username, password)
                flash('Created account')
                return redirect(url_for('login'))
        else:
            flash('Password needs to have stuff in it')
            return redirect(url_for("wanna_register"))
    elif len(username) == 0:
        flash("Username needs to have stuff in it")
        return redirect(url_for("wanna_register"))
    else:
        flash("Username already taken!")
        return redirect(url_for("wanna_register"))
    # TRY TO REGISTER AGAIN
    return render_template("wanna_register.html")

@app.route('/logout')
def logout():
    """Logs the user out"""
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('login'))
    session.pop(user, None)
    setUser(None)
    setSynced(False)
    return redirect(url_for('home'))

@app.route('/tracker')
def tracker():
    """Tracks calories."""
    if user not in session:
        flash('Please log in to access this page!')
        return redirect(url_for('login'))

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    """Displays settings page."""
    if user in session:
        data = db.DB_Manager(DB_FILE)
        intake_goal= 'empty, please set up your account!'
        if data.access_calorie_goal(user) != None: #means user has already setup account
            intake_goal= data.access_calorie_goal(user)
        return render_template("settings.html", loggedIn= True, intake_goal= intake_goal)

    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/goals', methods=['POST', 'GET'])
def goals():
    """Handles goal setting forms"""
    if user in session:
        data = db.DB_Manager(DB_FILE)
        if request.form["cal_intake"] != '':
            data.change_calorie_goal(user,request.form["cal_intake"])
            intake_goal= data.access_calorie_goal(user)
        return render_template("settings.html", loggedIn= True, intake_goal= intake_goal)
    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/main', methods=['POST', 'GET'])
def main():
    """Activities page."""
    if user in session:
        data = db.DB_Manager(DB_FILE)
        global userSynced
        profile=''
        if data.check_token(user): #if user has tokens, print their profile
            setSynced(True)
            user_id, auth_token= data.get_token(user)
            api.setUserId(str(user_id))
            api.setAccessToken(str(auth_token))
            api.setHeaders(str(auth_token))
            profile= api.fetchProfile(str(user_id))
            # print('yeet')
            #displaying heart rate
            heart = api.fetchHeartRateDP(str(user_id), 'today', '7d')['activities-heart']
            heart_data = json_normalize(heart)
            heart_data.drop(['value.customHeartRateZones'], axis=1)
            print(heart_data['value.heartRateZones'])
            # heart_rate_data = pd.DataFrame
            # print(heart, 'yeet')
        else:
            auth_token=request.args.get('token')
            user_id= request.args.get('user_id')
            if auth_token != None and user_id != None:
                setSynced(True)
                data.insert_token(user,user_id,auth_token) #user now has fitbit credentials!
                api.setUserId(str(user_id))
                api.setAccessToken(str(auth_token))
                api.setHeaders(str(auth_token))
                profile= api.fetchProfile(str(user_id))

        return render_template("home.html",profile=profile, synced=userSynced, loggedIn=True, heart_data_url=url_for('heart_rate'))
    profile= ""
    return render_template("home.html", profile= profile,synced=userSynced,loggedIn= False)

@app.route('/food', methods=['POST','GET'])
def food():
    """Handles requesting meals"""
    if user in session:
        data = db.DB_Manager(DB_FILE)
        global meals

        chosen_lst=[]
        meal_lst=[]

        in_goal= None
        curr_in_cal= None

        #Handles whether user set a goal + displaying how much is left to eat
        if data.access_calorie_goal(user) != None:
            in_goal= data.access_calorie_goal(user)
            curr_in_cal= data.cals_needed(user)
        else:
            flash('Please setup your goals in the settings page!')

        if 'meal_num' in request.form.keys():
            meals1 = request.form["meal_num"]
            if meals1 != '':
                if int(meals1) > 10 or int(meals1) < 1:
                    flash("Invalid Input!")
                else:
                    meals = meals1
                    cal_per_meal= int(curr_in_cal) / int(meals1)
                    meal_lst = f.getRandomMeals(str(0),str(cal_per_meal), meals1)

                    return render_template("food.html", loggedIn=True, food_lst = meal_lst, in_goal= in_goal, curr_in_cal=str(curr_in_cal))
        else:
            return render_template("food.html", loggedIn=True, food_lst = meal_lst,in_goal= in_goal, curr_in_cal=str(curr_in_cal))

        for i in range(1,int(meals) +1):
            if str(i) in request.form.keys():
                food = request.form[str(i)] #returns a str of tuple
                chosen_lst.append(eval(food))

        if len(chosen_lst)>0:
            for food in chosen_lst:
                cals_in= food[1]
                name= food[0]
                data.insert_calories_day(user,cals_in,name)

        return redirect(url_for('plan'))

    flash('Please log in to access this page!')
    return redirect(url_for('login'))


@app.route('/plan', methods=['POST', 'GET'])
def plan():
    """ Handles planning page using user's saved suggestions + additions """
    if user in session:
        data = db.DB_Manager(DB_FILE)

        in_goal= None
        curr_in_cal= None
        chosen_lst= []
        #Handles whether user set a goal + displaying how much is left to eat
        if data.access_calorie_goal(user) != None:
            in_goal= data.access_calorie_goal(user)
            curr_in_cal= data.cals_needed(user)
        else:
            flash('Please setup your goals in the settings page!')

        now = datetime.now().strftime('%Y/%m/%d') #gets current date

        if len(data.get_all_intake(user,now)) != 0: #seeing if user saved any meals
            chosen_lst= data.get_all_intake(user,now)
            print(str(chosen_lst))

        return render_template('plan.html',loggedIn= True, chosen_lst= chosen_lst, in_goal=in_goal, curr_in_cal=curr_in_cal)

    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/api/heart-rate')
def heart_rate():
    """
    REST endpoint for heart rate data.
    Meant to be passed into javascript using "data."
    """
    if user in session:
        user_id, auth_token= data.get_token(user)
        api.setUserId(str(user_id))
        api.setAccessToken(str(auth_token))
        api.setHeaders(str(auth_token))
        heart = api.fetchHeartRateDP(str(user_id), 'today', '30d')['activities-heart']
        heart_rate_data = []
        for entry in heart:
            if 'restingHeartRate' in entry['value'].keys():
                heart_rate_data.append(
                    {'datetime': entry['dateTime'], 'resting_heart_rate': entry['value']['restingHeartRate']}
                )
                # heart_rate_dict['datetime'].append(entry['dateTime'])
                # heart_rate_dict['resting_heart_rate'].append(entry['value']['restingHeartRate'])
        # print(heart_data)
        return jsonify(heart_rate_data)
    else:
        message = {
            'Error':'No username found!',
        }
        return jsonify(message)

    # TEST CODE FOR ENDPOINT
    # user = 'a'
    # user_id, auth_token= data.get_token(user)
    # api.setUserId(str(user_id))
    # api.setAccessToken(str(auth_token))
    # api.setHeaders(str(auth_token))
    # heart = api.fetchHeartRateDP(str(user_id), 'today', '30d')['activities-heart']
    # heart_rate_dict = {
    #     'datetime': [],
    #     'resting_heart_rate': [],
    # }
    # for entry in heart:
    #     if 'restingHeartRate' in entry['value'].keys():
    #         heart_rate_dict['datetime'].append(entry['dateTime'])
    #         heart_rate_dict['resting_heart_rate'].append(entry['value']['restingHeartRate'])
    # return jsonify(heart_rate_dict)

if __name__ == "__main__":
    app.debug = True
    app.run()
