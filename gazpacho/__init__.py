import json, urllib, os, sqlite3
from urllib.error import HTTPError

from flask import Flask, render_template, flash, request, session, redirect, url_for, jsonify
from pandas.io.json import json_normalize
import pandas as pd

import os
from datetime import datetime
from utils import db
from utils import api
from utils import food as f
# from utils import api
import random

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
recipes= 0

def setUser(userName):
    global user
    user = userName

def setSynced(bool):
    global userSynced
    userSynced= bool

def setMeals(val):
    global meals
    meals= val

def setRecipes(val):
    global recipes
    recipes= val

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
        if data.get_metric_user(user,'steps_goal') != None:
            step_goal= data.get_metric_user(user,'steps_goal')
        else:
            step_goal = 0
        if userSynced: #if user has tokens, print their profile, they are SYNCED
            user_id, auth_token= data.get_token(user)
            api.setUserId(str(user_id))
            api.setAccessToken(str(auth_token))
            api.setHeaders(str(auth_token))
            profile= api.fetchProfile(str(user_id))
            age= profile['user']['age'] #requested every time since you want to see refreshed data
            height= int(profile['user']['height'])
            weight= profile['user']['weight']
            gender = profile['user']['gender']
        else:
            if data.get_metric_user(user,'steps_goal') != None:
                step_goal= data.get_metric_user(user,'steps_goal')
            if data.get_metric_user(user,'height') != None:
                height=data.get_metric_user(user,'height')
            if data.get_metric_user(user,'weight') != None:
                weight=data.get_metric_user(user,'weight')
        return render_template("settings.html", loggedIn= True, intake_goal= intake_goal, synced=userSynced, heightU=height, weightU=weight, stepsU= step_goal)

    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/goals', methods=['POST', 'GET'])
def goals():
    """Handles goal setting forms"""
    data = db.DB_Manager(DB_FILE)
    intake_goal = data.get_metric_user(user,'in_calories_goal')
    heightU = data.get_metric_user(user, 'height')
    weightU = data.get_metric_user(user, 'weight')
    stepsU = data.get_metric_user(user, 'steps_goal')

    if user in session:
        data = db.DB_Manager(DB_FILE)
        print(request.form['height'])
        if request.form["cal_intake"] != '':
            data.set_metric_user(user,'in_calories_goal',request.form["cal_intake"])
            intake_goal= data.get_metric_user(user,'in_calories_goal')
        if request.form["height"] != '':
            data.set_metric_user(user,'height', request.form["height"])
            heightU= data.get_metric_user(user, 'height')
        if request.form["weight"] != '':
            data.set_metric_user(user,'weight',request.form["weight"])
            weightU= data.get_metric_user(user, 'weight')
        if request.form["steps"] != '':
            data.set_metric_user(user,'steps_goal',request.form["steps"])
            stepsU= data.get_metric_user(user, 'steps_goal')
        return render_template("settings.html", loggedIn= True, intake_goal= intake_goal, heightU = heightU, weightU = weightU, stepsU= stepsU, synced=userSynced )
    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/main', methods=['POST', 'GET'])
def main():
    """Home page"""
    if user in session:
        data = db.DB_Manager(DB_FILE)
        global userSynced

        #seen by unsynced users
        username= user
        height= "Unknown"
        weight= "Unknown"
        age= "Unknown"
        cal_goal= "Unknown"
        step_goal= "Unknown"
        cals_needed= "Unknown"

        if data.get_metric_user(user,'steps_goal') != None:
            step_goal= data.get_metric_user(user,'steps_goal')
        else:
            step_goal = 0

        if data.check_token(user): #if user has tokens, print their profile, they are SYNCED
            setSynced(True)
            user_id, auth_token= data.get_token(user)
            api.setUserId(str(user_id))
            api.setAccessToken(str(auth_token))
            api.setHeaders(str(auth_token))
            profile= api.fetchProfile(str(user_id))
            age= profile['user']['age'] #requested every time since you want to see refreshed data
            avg_steps= profile['user']['averageDailySteps']
            height= int(profile['user']['height'])
            weight= profile['user']['weight']
            gender = profile['user']['gender']
            if data.cals_needed(user) != -1:
                cals_needed =data.cals_needed(user)
            if data.get_metric_user(user,'in_calories_goal') != None:
                cal_goal= data.get_metric_user(user,'in_calories_goal')
            heart = api.fetchHeartRateDP(str(user_id), 'today', '7d')['activities-heart']
            heart_data = json_normalize(heart)
            heart_data.drop(['value.customHeartRateZones'], axis=1)
            #print(heart_data['value.heartRateZones'])
            return render_template("home.html",height=height, weight=weight, gender= gender, age= age, avg_steps= avg_steps, username= username, cals_needed=cals_needed, cal_goal=cal_goal, synced=userSynced, loggedIn=True)

        #fetching tokens from redirect
        elif request.args.get('token') != None and request.args.get('user_id') != None:
            auth_token=request.args.get('token')
            user_id= request.args.get('user_id')
            data.insert_token(user,user_id,auth_token) #user now has fitbit credentials!
            api.setUserId(str(user_id))
            api.setAccessToken(str(auth_token))
            api.setHeaders(str(auth_token))
            setSynced(True)
            profile= api.fetchProfile(str(user_id))
            age= profile['user']['age'] #requested every time since you want to see refreshed data
            avg_steps= profile['user']['averageDailySteps']
            height= int(profile['user']['height'])
            weight= profile['user']['weight']
            gender = profile['user']['gender']
            if data.cals_needed(user) != -1:
                cals_needed = data.cals_needed(user)
            if data.get_metric_user(user,'in_calories_goal') != None:
                cal_goal= data.get_metric_user(user,'in_calories_goal')
            return render_template("home.html",height=height, weight=weight, gender= gender, age= age, avg_steps= avg_steps, username= username, cals_needed=cals_needed, cal_goal=cal_goal, synced=userSynced, loggedIn=True)
            #otherwise, not synced
        else:
            if data.get_metric_user(user,'in_calories_goal') != None:
                cal_goal= data.get_metric_user(user,'in_calories_goal')
            if data.get_metric_user(user,'height') != None:
                height=data.get_metric_user(user,'height')
            if data.get_metric_user(user,'weight') != None:
                weight=data.get_metric_user(user,'weight')
            if data.cals_needed(user) != -1:
                cals_needed =data.cals_needed(user)
            return render_template("home.html",height=height, weight=weight, cal_goal= cal_goal, step_goal= step_goal, cals_needed= cals_needed, username= username, synced=userSynced, loggedIn=True)

    flash("Please Log In or Register to Continue!")
    return render_template("home.html", synced=userSynced,loggedIn= False)

@app.route('/unsync', methods=['POST','GET'])
def unsync():
    data = db.DB_Manager(DB_FILE)
    data.delete_token(user)
    setSynced(False)
    flash('You are no longer synced to your Fitbit!')
    return redirect(url_for('main'))


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

                    if data.cals_needed(user) > 0:
                        meal_lst = f.getRandomMeals(str(cal_per_meal*.9),str(cal_per_meal), meals1)
                        return render_template("food.html", loggedIn=True, food_lst = meal_lst, in_goal= in_goal, curr_in_cal=str(curr_in_cal), synced= userSynced)

                    else:
                        flash('You have reached your daily calorie limit!')
                        return render_template("recipe.html", loggedIn=True, food_lst = meal_lst, in_goal= in_goal, curr_in_cal=str(curr_in_cal), synced=userSynced)
        else:
            return render_template("food.html", loggedIn=True, food_lst = meal_lst,in_goal= in_goal, curr_in_cal=str(curr_in_cal),synced= userSynced)

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

@app.route('/recipe', methods=['POST','GET'])
def recipe():
    """Handles requesting meals from recipe API (returns healthier options and no alcohol!)"""
    if user in session:
        data = db.DB_Manager(DB_FILE)
        global recipes

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
            meals2 = request.form["meal_num"]
            if meals2 != '':
                if int(meals2) > 10 or int(meals2) < 1:
                    flash("Invalid Input!")
                else:
                    recipes = meals2
                    cal_per_meal= int(curr_in_cal) / int(meals2)

                    if data.cals_needed(user) > 0:
                        meal_lst = f.getRandomRecipes(str(int(cal_per_meal*.9)),str(int(cal_per_meal)), meals2) #lol this had an int issue im sad now
                        return render_template("recipe.html", loggedIn=True, food_lst = meal_lst, in_goal= in_goal, curr_in_cal=str(curr_in_cal),synced=userSynced)
                    else:
                        flash('You have reached your daily calorie limit!')
                        return render_template("recipe.html", loggedIn=True, food_lst = meal_lst, in_goal= in_goal, curr_in_cal=str(curr_in_cal),synced=userSynced)
        else:
            return render_template("recipe.html", loggedIn=True, food_lst = meal_lst,in_goal= in_goal, curr_in_cal=str(curr_in_cal), synced=userSynced)

        for i in range(1,int(recipes) +1):
            if str(i) in request.form.keys():
                food = request.form[str(i)] #returns a str of tuple
                chosen_lst.append(eval(food))

        if len(chosen_lst)>0:
            for food in chosen_lst:
                cals_in= food[1]
                name= food[0]
                #ingredients= food[2]
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
        chosen_lst= data.get_all_intake(user,now)
        if len(chosen_lst) != 0: #seeing if user saved any meals
            print(str(chosen_lst))
        full_lst = sorted(data.get_all_intake(user))[::-1] # get the entire list of stuff and reverse it to get the most recent data
        full_matching_list = [(food, calories) for timestamp, food, calories in full_lst] # match the dimensions of chosen_lst
        # if chosen_lst and full_lst are equal to each other, do not spawn a graph

        graph_spawn = False
        food_url = None
        if set(chosen_lst) != set(full_matching_list):
            graph_spawn = True
            food_url = url_for('food_history')
        return render_template('plan.html',loggedIn= True, chosen_lst= chosen_lst, in_goal=in_goal, curr_in_cal=curr_in_cal, full_lst=full_lst, synced=userSynced, graph_spawn = graph_spawn, food_url=food_url)

    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/user_meal', methods=['POST', 'GET'])
def user_meal():
    """ Handles saving user's additions to db """
    if user in session:
        data = db.DB_Manager(DB_FILE)

        if 'user_meal' in request.form.keys() and 'user_cal' in request.form.keys(): #extra security
            meal_name= request.form['user_meal']
            user_cal= request.form['user_cal']
            if meal_name == '' or user_cal== '':
                flash("Please fill out both fields! (To the best of your ability)")
            else:
                if data.access_calorie_goal(user) != None:
                    if int(user_cal) <= data.cals_needed(user):
                        data.insert_calories_day(user,user_cal,meal_name)

                    else:
                        flash("That's too many calories! You may have reached your daily goal!")

        return redirect(url_for('plan'))

    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/delete-meal/<meal>/<int:cals>', methods=['GET','POST'])
def cancel_meal(meal, cals):
    """Deletes a meal."""
    if user in session:
        meal = meal.replace('%20', ' ')
        if data.delete_meal(user, meal, cals):
            flash('Meal successfully deleted!')
            return redirect(url_for('plan'))
        else:
            flash('Please log in to access this page!')
            return redirect(url_for('login'))
    flash('Please log in to access this page!')
    return redirect(url_for('login'))

@app.route('/activity', methods=['POST', 'GET'])
def activity():
    global userSynced
    if user in session:
        data = db.DB_Manager(DB_FILE)
        stepG = data.get_metric_user(user, 'steps_goal')
        stepLeft = stepG
        if 'stepIn' in request.form.keys():
            if request.form["stepIn"] != '':
                stepLeft = stepLeft - int(request.form["stepIn"])
                if stepLeft < 0:
                    flash('You Reached Your Step Goal!')
            return render_template('activity.html',loggedIn= True, userSynced=userSynced, stepG =stepG, stepLeft = stepLeft, heart_data_url=url_for('heart_rate'), steps_url=url_for('steps'),synced=userSynced)
        return render_template('activity.html',loggedIn= True, userSynced=userSynced, stepG =stepG, heart_data_url=url_for('heart_rate'), steps_url=url_for('steps'),synced=userSynced)

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
                    {'dateTime': entry['dateTime'], 'value': entry['value']['restingHeartRate']}
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

@app.route('/api/steps')
def steps():
    """
    REST endpoint for steps data.
    Meant to be passed into javascript using "data."
    """
    if user in session:
        user_id, auth_token= data.get_token(user)
        api.setUserId(str(user_id))
        api.setAccessToken(str(auth_token))
        api.setHeaders(str(auth_token))
        steps = api.fetchStepData(str(user_id), 'today', '30d')["activities-steps"]
        return jsonify(steps)
    else:
        message = {
            'Error':'No username found!',
        }
        return jsonify(message)

@app.route('/api/food')
def food_history():
    """
    REST endpoint for food/calorie data.
    Meant to be passed into javascript using "data."
    """
    # smpl = ['2019/06/07', '2019/06/05','2019/06/04', '2019/06/08']
    # user = 'b'
    if user in session:
        global data
        food_hist = data.get_all_intake(user)
        food_lst = []
        # create the mapping needed to load into a dataframe
        for entry in food_hist:
            food_lst.append({'dateTime': entry[0], 'calories': entry[2]})
            # food_lst.append({'dateTime': random.choice(smpl), 'calories': random.randint(0, 700)})
        # return a json containing total calorie consumption per day
        food_df = pd.DataFrame(food_lst)
        sum_df = food_df.groupby('dateTime')['calories'].sum()
        sum_df = pd.DataFrame(sum_df) # was a Series, now a DF
        sum_df.rename(columns={'calories':'value'}, inplace=True)
        food_json = json.loads(sum_df.to_json(orient='table'))['data']
        return jsonify(food_json)
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
