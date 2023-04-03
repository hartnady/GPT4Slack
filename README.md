# GPT4Slack

## Routing.py
Main flask routing definitions for the Slack App endpoints
You will need to configure your Slack app settings as follows:
Interactivity URL: https://your_account.pythonanywhere.com/slack/interactivity
Events URL: https://your_account.pythonanywhere.com/slack/events
Slash Command: https://your_account.pythonanywhere.com/slack/slash_command

## QueueWorker.py
Coordinates picking items off the queue from MySQL and processing them
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
