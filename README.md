# teeskentelee_suuruutta
### Shafali Gupta, Aleksandra Koroza, Raunak Chowdhury, Hasif Ahmed
### Period 8
## What is this?

FitByBit is a website that tracks your calories and your activity by either linking your account to your fitbit or through user input. It reccomends meals and tracks your progress daily. We offer two different meal suggesting mechanisms (Binge and Health(ier)). Try them out for yourself!

## What if I don't have a Fitbit!

Never fear. You can create a free account [here](https://accounts.fitbit.com/signup?lcl=en_US&targetUrl=https%3A%2F%2Fwww.fitbit.com%2Flogin%2Ftransferpage%3Fredirect%3Dhttps%25253A%25252F%25252Fwww.fitbit.com%25252F) and sync to it when prompted on our website. You can manually log step and heart rate data from their interface. If you don't, you'll miss out on some pretty cool graphs.

## Packages Included
- Flask: Our python microframework that allows us to build our website
- pandas: A data science library. We used this to aggregate the total calorie consumption per day in order to generate a graph.

## Launch Instructions
### Install and Run on Localhost
1. Clone repository

     `$ git clone https://github.com/shafali731/teeskentelee_suuruutta.git`

2. Install Python 3.7.1 from [here](https://www.python.org/downloads/) if you haven't already.
3.  Install virtualenv by running

     `$ pip install virtualenv`

  - Make a new venv

      `$ python3 -m venv ENV_DIR`

  - Activate it  

      `$ . /ENV_DIR/bin/activate `

  - Deactivate it  

      `$ deactivate`  

 4. Run in the FitByBit/ folder using an active virtualenv   

      `$ pip install -r requirements.txt`

 5. Run the flask app

      `$ python __init__.py `

 6. Go [here](http://127.0.0.1:5000/) to see the website!

### Install and run on Apache2
1. Clone the repository in the `/var/www/` directory

    `$ git clone https://github.com/shafali731/teeskentelee_suuruutta.git FitByBit`
 4. Install the requirements in `/var/www/FitByBit/FitByBit` directory

      `$ pip install -r requirements.txt`

2. Run the following commands on the folder `FitByBit`

    `$ chgrp -R www-data FitByBit`
    `$ chmod -R g+w FitByBit`

3. Move the `.conf` file

    `$ mv /var/www/FitByBit/FitByBit.conf /etc/apache2/sites-available/`

4. Enable the site in Apache

    `$ a2ensite appname`

5. Reload/Restart Apache

    `$ service apache2 reload`
      or
    `$ service apache2 restart`

6. Connect to the server IP.

### API Keys
In order to ensure the site works correctly, you must procure the API keys and store them in the correct locations.

1. Procure your API credentials from the Recipe Search API (instructions [here](https://github.com/shafali731/teeskentelee_suuruutta/blob/master/doc/api_EDAMAM_Recipe_Search.pdf)). and  to procure the keys. One

1. Create a file named `recipe.json` in the `keys` directory with the following information:
``` json
{
    "rec_key": "YOUR API KEY HERE",
    "rec_id": "YOUR API ID HERE"
}
```

1. Procure your API credentials from the Food and Grocery API (instructions [here](https://github.com/shafali731/teeskentelee_suuruutta/blob/master/doc/api_EDAMAM_Food_and_Grocery_Database.pdf)).

1. Create a file named `food.json` in the `keys` directory with the following information:
``` json
{
    "key": "YOUR API KEY HERE",
    "id": "YOUR API ID HERE"
}
```
