#lambBaaas -- Hui Min Wu, Raunak Chowdhury, Anton Danylenko
#SoftDev1 pd8
#P02 -- The End

import sqlite3   # enable control of an sqlite database

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
            create_table()
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
    #========================HELPER FXNS=======================
    #===========================DB FXNS========================

    def create_users(self):
        """
        CREATES TABLE OF users
        """
        user_fields = ('user_name TEXT PRIMARY KEY', 'password TEXT', 'email TEXT',\
         'gender TEXT', 'calories_spent INT', 'amt_spent INT',\
         'budget INT', 'pts INT', 'height INT', 'weight INT',\
         'total_sleep_acquired INT')
        self.tableCreator('users', *user_fields)
        return True

    def create_meals(self):
        """
        CREATES TABLE OF USERS and MEALS
        """
        meal_fields = ('user_name TEXT', 'course TEXT', 'meal_desc TEXT', 'calories INT', 'cost INT', 'timestamp TEXT')
        self.tableCreator('typing', *meal_fields)
        return True

    def create_activities(self):
        '''
        CREATES TABLE OF ACTIVITIES
        '''
        activity_fields = ('user_name TEXT', 'activity_name TEXT', 'timestamp TEXT')
        self.tableCreator('activities', *activity_fields)
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
            row = (userName, password)
            self.insert_row('users', ('user_name', 'password'), row)
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

    def getWPM(self, userName, difficulty):
        '''
        GETS the current wpm saved for the user in the database.
        '''
        c = self.openDB()
        command_tuple = (userName, difficulty)
        c.execute("INSERT INTO typing VALUES(?, 0, 0, ?)", command_tuple)
        c.execute("SELECT wpm FROM typing WHERE (user_name = ? AND difficulty = ?)", command_tuple)
        currentWPMs = c.fetchall()
        for wpm in currentWPMs:
            if (wpm[0]!=0):
                return wpm[0]
        return 0

    def saveWPM(self, userName, wpm, timestamp, difficulty):
        '''
        SAVES wpm, timestamp, and difficulty for username
        '''
        c = self.openDB()
        command_tuple = (userName,difficulty)
        c.execute("INSERT INTO typing VALUES(?, 0, 0, ?)", command_tuple)
        c.execute("DELETE FROM typing WHERE (user_name = ? AND difficulty = ?)", command_tuple)
        command_tuple = (userName, wpm, timestamp, difficulty)
        c.execute("INSERT INTO typing VALUES(?,?,?,?)", command_tuple)
        self.save()
        return True

    def saveWord(self, userName, word):
        '''
        SAVES word each user wants to save
        '''
        c = self.openDB()
        command_tuple = (userName,word)
        c.execute("INSERT INTO vocab VALUES (?,?)", command_tuple)
        self.save()
        return True

    def saveAct(self, userName, activity, category, part):
        '''
        SAVES activity
        '''
        c = self.openDB()
        command_tuple = (userName,activity,category,part)
        c.execute("INSERT INTO activities VALUES (?,?,?,?)",command_tuple)
        self.save()
        return True

    def getActivities(self, userName):
        '''
        RETURNS activities of user
        '''
        c = self.openDB()
        acts = {'activity':[], 'category':[], 'part':[]}
        c.execute("SELECT activity FROM activities WHERE user_name='{0}' ORDER BY category".format(userName))
        acts['activity'] = c.fetchall()
        c.execute("SELECT category FROM activities WHERE user_name='{0}' ORDER BY category".format(userName))
        acts['category'] = c.fetchall()
        c.execute("SELECT part FROM activities WHERE user_name='{0}' ORDER BY category".format(userName))
        acts['part'] = c.fetchall()
        return acts

    def deleteAct(self, userName, activity):
        c = self.openDB()
        command_tuple = (activity,userName)
        c.execute("DELETE FROM activities WHERE activity=? AND user_name=?", command_tuple)
        self.save()
        return True

    def deleteWord(self, userName, word):
        c = self.openDB()
        command_tuple=(word, userName)
        c.execute("DELETE FROM vocab WHERE word=? AND user_name=?", command_tuple)
        self.save()
        return True

    def getLeaderboard(self):
        '''
        RETURNS leaderboard of users
        '''
        c = self.openDB()
        command = "SELECT * FROM typing WHERE wpm != 0 ORDER BY wpm DESC"
        c.execute(command)
        return c.fetchall()

    def getVocabWords(self, user):
        '''
        RETURNS all of user's vocab's words
        '''
        # prINT("getting list")
        c = self.openDB()
        c.execute("SELECT word FROM vocab WHERE user_name=?", (user))
        return c.fetchall()