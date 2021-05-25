# Fampay-Youtube
 Youtube API Hiring Assignment

This application has been created using Python-Flask framework.

### ALready hosted on HEROKU
 - **Set the Search topic** -> https://fampay-youtube.herokuapp.com/search?query=football
 - **Dashboard** -> https://fampay-youtube.herokuapp.com/dashboard
 - **Pagination** in Dashboard -> https://fampay-youtube.herokuapp.com/dashboard/?pageNumber=2&maxResults=2
 - **Stop Synchronisation from Youtube** -> https://fampay-youtube.herokuapp.com

### Pre-requisites
 - Python 3.6 or newer
 - pip should be installed

### Instructions to setup the server

##### Step 1
DOWNLOAD and EXTRACT the gti repo OR FORK -> CLONE the repo

##### Step 2
Open Terminal and cd into the repo folder

##### Step 3 : Setting up the virtual environment
```
python3 -m venv venv
```

##### Step 4 : Activate the virtual environment
```
source venv/bin/activate
```

##### Step 5 : Install the requirements.txt
```
pip install -r requirements.txt
```

##### Step 6 : Setup the Environment variable for FLASK_APP
```
export FLASK_APP=app.main:create_app
```

##### Step 7 : Start the server
```
flask run
```
