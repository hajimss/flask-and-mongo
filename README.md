# flask-and-mongo

### Introduction
This application serves as a platform for me to experiment with Flask and the web-development elements that come along with it (eg. Jinja2 templating engine, ). MongoDB is the preferred database since it is a small scale project that does not contain vast amount of collections and data. Furthermore, it is easy to implement with the JSON-like documents.

### Overall Architecture
Overall web app framework: Flask
Frontend framework: HTML, CSS and Jinja2(injection of python codes & variables)
Backend database: MongoDB

WSGI Server: Gunicorn
 - For communication between web servers and the python application

### Endpoints
Method: POST
Endpoint: /createuser
Usage: To create a new user
Remarks: Users are transalted to friends which can be viewed in the /friends endpoint

Method: GET
Endpoint: /friends
Usage: To view the list of friends/user

Method: DELETE
Endpoint: /deleteuser/<user>
Usage: To delete the specific friend/user from the list

Method: POST
Endpoint: /journal
Usage: To create a journal entry

Method: GET 
Endpoint: /journal
Usage: To view the list of journal entries and its contents

Method: POST 
Endpoint: /upload_csv
Usage: To upload a csv and store its contents

Method: GET 
Endpoint: /upload_csv
Usage: To view the list of names of stored csv

Method: GET 
Endpoint: /expand_csv
Usage: To view the csv in a dataframe

### Running App
How to run it locally:
1. Ensure that you have python3 installed. Refer to this documentation for steps to set up python: https://realpython.com/installing-python/

2. Clone this repository to your local machine and ensure you have the specific dependencies by installing using the command stated below.
```
git clone https://github.com/hajimss/flask-and-mongo.git
```
```
pip install -r requirements.txt
```
3. Set the environment variable MONGO_URL to your own Cluster connection string obtained in your cloud mongodb account.
MacOS:
```
export MONGO_URL="mongodb+srv://XXXX"
```
For Windows, refer to this page for instructions on the specific OS version to setup you MONGO_URL variable:
https://www.schrodinger.com/kb/1842
4. Once done, run server.py to have the app running on your local machine.
```
python server.py
```


The web app is deployed on heroku so do have a look!
https://hazimisusingflaskandmongo.herokuapp.com/home

Cheers!
