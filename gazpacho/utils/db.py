import sqlite3   # enable control of an sqlite database
from datetime import datetime

class DB_Manager:
    '''
    HOW TO USE:
    Every method openDB by connecting to the inputted path of
    a database file. After performing all operations on the
    database, the instance of the DB_Manager must save using
    the save method.
    The operations/methods can be found below. DB_Manager
    has been custom fitted to work with
    P00 -- Da Art of Storytellin'
    '''

    def __init__(self, dbfile):

        #SET UP TO READ/WRITE TO DB FILES
        self.DB_FILE = dbfile
        self.db = None

        # set up the tables
        for create_table in [self.create_users, self.create_meals, self.create_activities]:
            if not create_table():
                raise BaseException('Something went wrong!')
    #========================HELPER FXNS=======================

    def openDB(self):
        """
        OPENS DB_FILE AND RETURNS A CURSOR FOR IT
        """
        self.db = sqlite3.connect(self.DB_FILE) # open if file exists, otherwise create
        return self.db.cursor()

    def tableCreator(self, tableName, *args):
        """
        GENERALIZED TABLE CREATOR USING *ARGS
        Meant for dev calls only
        """
        c = self.openDB()
        if not self.isInDB(tableName):
            command = "CREATE TABLE '{}' (" # ({1}, {2});")".format(tableName, col0, col1)
            for i in range(len(args)):
                command += '{},'
            command = command[:-1] # strip off last comma
            command += ');' # throw in end statement
            command = command.format(tableName, *args) # creates (tableName, col0, col1,...)
            c.execute(command)

    def insert_row(self, tableName, fields, data):
       """
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @fields are the columns being added to
         @data is a tuple containing data to be entered into those fields
       """
       c = self.openDB()
       command = "INSERT INTO '{}' ("
       # print(fields, len(fields), ('{},'* len(fields)))
       command += ('{},'* len(fields))[:-1] #extends fields in SQL statement by the # of fields given
       command += ') VALUES (' # throw in VALUES
       command += ('?,' * len(data))[:-1] #extends results by len(results)
       command += ');'
       # print(command)
       # vals = " VALUES(?, ?)"
       c.execute(command.format(tableName, *fields), data)
       self.save()

    def isInDB(self, tableName):
        '''
        RETURNS True IF THE tableName IS IN THE DATABASE
        RETURNS False OTHERWISE
        '''
        c = self.openDB()
        command = "SELECT * FROM sqlite_master WHERE type = 'table'"
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all tableNames and store in a set
        tableNames = set([x[1] for x in selectedVal])

        return tableName in tableNames

    def table(self, tableName):
        '''
        PRINTS OUT ALL ROWS OF INPUT tableName
        '''
        c = self.openDB()
        command = "SELECT * FROM '{0}'".format(tableName)
        c.execute(command)
        return c.fetchall()

    def save(self):
        '''
        COMMITS CHANGES TO DATABASE AND CLOSES THE FILE
        '''
        self.db.commit()
        self.db.close()
        self.db = None
    #========================HELPER FXNS=======================
    #===========================DB FXNS========================

    def create_users(self):
        """
        CREATES TABLE OF users
        """
        user_fields = ('user_name TEXT PRIMARY KEY', 'password TEXT', 'email TEXT',\
         'gender TEXT', 'in_calories_goal INT', 'out_calories_goal INT',\
         'budget INT', 'pts INT', 'height INT', 'weight INT', 'steps_goal INT'\
         'total_sleep_acquired INT', 'auth_token TEXT', 'user_id TEXT')
        self.tableCreator('users', *user_fields)
        return True

    # def create_meals(self):
    #     """
    #     CREATES TABLE OF USERS and MEALS
    #     """
    #     meal_fields = ('user_name TEXT', 'course TEXT', 'meal_desc TEXT', 'calories INT', 'cost INT', 'timestamp TEXT')
    #     self.tableCreator('meals', *meal_fields)
    #     return True

    def create_activities(self):
        """
        CREATES TABLE OF ACTIVITIES
        """
        activity_fields = ('user_name TEXT', 'activity_name TEXT', 'timestamp TEXT', 'calories_out INT', 'steps INT')
        self.tableCreator('activities', *activity_fields)
        return True

    def create_meals(self):
        """
        CREATE TABLE OF CALORIE MEALS
        """
        log_fields = ('user_name TEXT', 'food_name TEXT', 'timestamp TEXT', 'calories_in INT')
        self.tableCreator('MEALS', *log_fields)
        return True

    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS'
        '''
        c = self.openDB()
        command = "SELECT user_name, password FROM users"
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def registerUser(self, userName, password):
        '''
        ADDS user TO DATABASE
        '''
        c = self.openDB()
        # userName is already in database -- do not continue to add
        if self.findUser(userName):
            return False
        # userName not in database -- continue to add
        else:
            row = (userName, password, 2000)
            self.insert_row('users', ('user_name', 'password', 'in_calories_goal'), row)
            return True

    def findUser(self, userName):
        '''
        CHECKS IF userName IS UNIQUE
        '''
        return userName in self.getUsers()

    def verifyUser(self, userName, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        command = "SELECT user_name, password FROM users WHERE user_name = {0}".format("'" + userName + "'")
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal == None:
            return False
        if userName == selectedVal[0] and password == selectedVal[1]:
            return True
        return False

    def set_metric_user(self, user, column, new_value):
        """
        updates a certain column of the USER table.
        Assumes 'column' exists in the table.
        """
        conn = sqlite3.connect(self.DB_FILE)
        c = conn.cursor()
        if self.findUser(user):
            command = "UPDATE USERS SET {} = ? WHERE user_name = ?;".format(column)
            command_tuple = (new_value, user)
            c.execute(command, command_tuple)
            # self.save()
            conn.commit()
            return True
        return False

    def get_metric_user(self, user, column):
        """
        gets a certain column of the USER table.
        Assumes 'column' exists in the table.
        """
        c = self.openDB()
        if self.findUser(user):
            command = "SELECT {} FROM USERS WHERE user_name = ?;".format(column)
            command_tuple = (user)
            c.execute(command, command_tuple)
            return c.fetchall()[0][0]
        return


    def insert_token(self, user, user_id, auth_token):
        """ Inserts user_id and auth_token of a user into DB """
        # c = self.openDB()
        conn = sqlite3.connect(self.DB_FILE)
        c = conn.cursor()
        if self.findUser(user):
            command = "UPDATE USERS SET user_id = ?, auth_token = ? WHERE user_name = ?;"
            command_tuple = (user_id, auth_token, user)
            c.execute(command, command_tuple)
            # self.save()
            conn.commit()
            return True
        return False

    def check_token(self, user):
        """
        Checks to see if the user has the necessary credentials for the fitbit.
        Returns True if the credentials exist, else False
        """
        c = self.openDB()
        command = "SELECT user_id, auth_token FROM USERS WHERE user_name = ?;"
        c.execute(command, (user,))
        user_id, auth_token = c.fetchall()[0]
        return user_id is not None and auth_token is not None

    def get_token(self, user):
        """ Returns auth_token and user_id of the user if exists """
        c = self.openDB()
        if self.check_token(user):
            command = "SELECT user_id, auth_token FROM USERS WHERE user_name = ?;"
            c.execute(command, (user,))
            user_id, auth_token = c.fetchall()[0]
            return user_id, auth_token
        return ()

    def delete_token(self, user):
        """ yeets tokens from db if they exist. If successful, returns True else False"""
        if not self.check_token(user):
            return False
        conn = sqlite3.connect(self.DB_FILE)
        c = conn.cursor()
        command = "UPDATE USERS SET user_id = NULL, auth_token = NULL WHERE user_name = ?;"
        c.execute(command, (user,))
        conn.commit()
        return True

    def insert_calories_day(self, user, cals_in, foodName):
        """
        Inserts one meals' worth of calorie intake into the table.
        if cals_in isn't an integer, return False else True
        """
        try:
            cals_in = int(cals_in)
        except ValueError:
            return False
        now = datetime.now().strftime('%Y/%m/%d')
        # print(now)
        row = (user, foodName, now, cals_in)
        columns_added = ('user_name', 'food_name', 'timestamp', 'calories_in')
        self.insert_row('meals', columns_added, row)
        return True

    def get_cal_intake(self, user, date):
        """ returns the calorie intake for a user in a given date. """
        total_intake = 0
        c = self.openDB()
        command = "SELECT calories_in FROM MEALS WHERE user_name = ? AND timestamp = ?;"
        c.execute(command, (user,date))
        for intake_value in c:
            # print(intake_value[0])
            total_intake += int(intake_value[0])
        return total_intake

    def get_all_intake(self, user, date):
        """ returns a list of calorie intake for a user in a given date. """
        total_intake = 0
        c = self.openDB()
        command = "SELECT food_name, calories_in FROM MEALS WHERE user_name = ? AND timestamp = ?;"
        c.execute(command, (user,date))
        entries = [[food_name, calories_in] for food_name, calories_in in c]
        return entries

    def get_cal_outtake(self, user, date):
        """ returns the calorie outtake and their food for a user in a given date. """
        total_outtake = 0
        c = self.openDB()
        command = "SELECT calories_out FROM ACTIVITIES WHERE user_name = ? AND timestamp = ?;"
        c.execute(command, (user,date))
        for outtake_value in c:
            total_outtake += int(outtake_value[0])
        return total_outtake

    def get_all_outtake(self, user, date):
        """ returns a list of calorie outtake for a user in a given date. """
        total_intake = 0
        c = self.openDB()
        command = "SELECT activity_name, calories_out FROM MEALS WHERE user_name = ? AND timestamp = ?;"
        c.execute(command, (user,date))
        entries = [[activity_name, calories_in] for activity_name, calories_in in c]
        return entries

    def access_calorie_goal(self, user):
        """ Pull in_calories_goal from USERS table """
        c = self.openDB()
        if self.findUser(user):
            command = "SELECT in_calories_goal FROM USERS WHERE user_name = ?;"
            c.execute(command, (user,))
            calories_goal = c.fetchall()[0][0]
            # print(calories_goal)
            return calories_goal
        return None # if no goal exists

    def cals_needed(self,user):
        """ Returns the # of calories needed to reach the calorie goal. """
        if self.findUser(user):
            cal_goal = self.access_calorie_goal(user)
            now = datetime.now().strftime('%Y/%m/%d')
            intake = self.get_cal_intake(user, now)
            diff = cal_goal - intake
            return diff if diff > 0 else 0
        return -1 # if no user exists

    # def change_calorie_goal(self, user, new_calorie_goal):
    #     # c = self.openDB()
    #     conn = sqlite3.connect(self.DB_FILE)
    #     c = conn.cursor()
    #
    #     if self.findUser(user):
    #         command = "UPDATE USERS SET in_calories_goal = ? WHERE user_name = ?;"
    #         # print(new_calorie_goal, user)
    #         c.execute(command, (new_calorie_goal, user))
    #         # self.save()
    #         conn.commit()
    #         return True
    #     return False
