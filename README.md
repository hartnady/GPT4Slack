# GPT4Slack

## Overall Architecture
Link coming soon

## Hosting & App Installation
This app is designed to be hosted on a FREE Python Anywhere account <br/>
Please sign up for your own Python Anywhere account here: www.pythonanywhere.com <br/>
Once you've created your account, go to the "Files" section and create a new folder (e.g. "slack") and upload these files there.

## MySQL
From your Python Anywhere console, you will need to install a new MySQL instance. Keep the database name as default. <br/>
Once you've supplied a username and password, you will need to add them to the config.py file.

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
Coordinates picking items off the queue from MySQL and processing them <br/>
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
