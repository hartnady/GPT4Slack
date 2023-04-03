# Database setup
username = "your_username"
password = "your_password"
hostname = f"{username}.mysql.pythonanywhere-services.com"
databasename = f"{username}$default"

SQLALCHEMY_DATABASE_URI = (
    f"mysql://{username}:{password}@{hostname}/{databasename}"
)
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 299}
SQLALCHEMY_TRACK_MODIFICATIONS = False

SLACK_WEBHOOK_URI = "https://hooks.slack.com/services/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" #General webhook for posting to the GPT bot user in Slack
SLACK_API_KEY = "put_your_slack_bot_api_key_here"
OPEN_AI_KEY = "put_your_openai_api_key_here"
CHAT_BOT_USER_ID = "U04RH1Y8NLB" #This is the user ID of your app's bot

ERROR_SERVICE_SENDER = 'NOTIFICATION_SENDER@email_address.com' #Replace this with a valid email address you will send notifications FROM
ERROR_SERVICE_SENDER_TOKEN = 'ufhtxyjubopekfqb' #Please research how to allow Python to send email using your Gmail account and replace this token
ERROR_SERVICE_RECIPIENT = 'NOTIFICATION_RECIPIENT@email_address.com' #Replace this with a valid email address you will send notifications TO
