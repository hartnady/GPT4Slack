# GPT4Slack

## Overall Architecture
Link coming soon

## Hosting & App Installation
This app is designed to be hosted on a FREE Python Anywhere account <br/>
Please sign up for your own Python Anywhere account here: www.pythonanywhere.com <br/>
Once you've created your account, go to the "Files" section and create a new folder (e.g. "slack") and upload these files there. <br/>
Then, create a new Web App by navigating to the "Web" section and following the on-screen instructions. You will need to specify the "Routing.py" file as the main app file for your Flask web app. To do this, go back to the "Web" section and scroll to "WSGI configuration file" and edit the file. Make sure it looks like this:
<pre>
import sys

# add your project directory to the sys.path
project_home = '**/home/vrpinc/slack**'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from **Routing** import app as application  
</pre>

## MySQL
From your Python Anywhere console, you will need to install a new MySQL instance. Keep the database name as default. <br/>
Once you've supplied a username and password, you will need to add them to the config.py file.
You will also need to create a "jobs" table in your database.
Open a new MySQL console for your database and enter the following commands:
<pre>CREATE TABLE jobs (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    slug VARCHAR(64) NOT NULL,
    state VARCHAR(10) NOT NULL DEFAULT 'queued',
    result INT(11) DEFAULT 0,
    webhook_url VARCHAR(500),
    message TEXT,
    user_id VARCHAR(20),
    response TEXT,
    channel_id VARCHAR(20)
);</pre>


## Dependencies
For these Python files to run correctly, you will need to install the "openai" module. </br>
To do so, open a bash prompt and type "pip install openai" </br>
The flask, sql_alchemy and other modules should already be installed.

# Files

## Routing.py
Main flask routing definitions for the Slack App endpoints <br/>
You will need to configure your Slack app settings as follows: <br/>
Interactivity URL: https://your_account.pythonanywhere.com/slack/interactivity <br/>
Events URL: https://your_account.pythonanywhere.com/slack/events <br/>
Slash Command: https://your_account.pythonanywhere.com/slack/slash_command 

## QueueWorker.py
Picks items off the queue from the MySQL "jobs" table and processes them <br/>
The inspiration for this design pattern came from https://blog.pythonanywhere.com/198

## Templates.py
Contains all the Slack Markdown for modals, App home page and other UI/UX elements

## config.py
Contains credentials for Slack, MySQL and OpenAI (consider moving to environment variables for production environment)

## Similar Projects
If you would like to implement the same App using Node.js and Firebase (instead of Python, Flask and MySQL) checkout:
https://github.com/magician11/openai-slack

## Contact
mark.hartnady@vrpconsulting.com
