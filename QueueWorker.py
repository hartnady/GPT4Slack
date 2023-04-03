import smtplib
from email.message import Message
from email.utils import formataddr
from smtplib import SMTPAuthenticationError

import requests, openai #, traceback
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS
from config import OPEN_AI_KEY, SLACK_API_KEY, CHAT_BOT_USER_ID, SLACK_WEBHOOK_URI
from config import ERROR_SERVICE_SENDER, ERROR_SERVICE_SENDER_TOKEN, ERROR_SERVICE_RECIPIENT
from Routing import Job

openai.api_key = OPEN_AI_KEY

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, **SQLALCHEMY_ENGINE_OPTIONS
)
Session = sessionmaker(engine)

def send_email(sender_email, sender_password, receiver_email, subject, body, sender_name='PythonAnywhere Exception'):
    try:
        # Create the message object
        message = Message()
        message['From'] = formataddr((sender_name, sender_email)) if sender_name else sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.set_payload(body)

        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Login to the SMTP server
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)  # Send the email
    except SMTPAuthenticationError as e:
        print(f"Failed to send email due to authentication error: {e}")
    except Exception as e:
        print(f"Failed to send email due to an error: {e}")

def gpt_chat(prompt):
    params = {
        "model": "gpt-3.5-turbo",
        "max_tokens":4097-len(prompt)-100,
        "temperature":0.5,
        "messages": [{"role": "user", "content": f"{prompt}"}]
    }
    try:
        response = openai.ChatCompletion.create(**params)

        if 'error' in response:
            error_message = response['error']['message']
            return f"GPT Error: {error_message}"
        else:
            completion_text = response.choices[0]['message']['content'].strip()
            return completion_text
    except Exception as e:
        #error_traceback = traceback.format_exc()
        return f"The GPT API is not responding.\nPlease check https://status.openai.com\n{str(e)}"
        #\n\nStack trace:\n{error_traceback}"

def find_pending_job():
    with Session.begin() as session:
        queue = session.query(Job).filter_by(state="queued")
        if job := queue.first():
            job.state = "processing"
            job.response = "Processing..."
            return job.id

def bot_is_member_of_channel(channel_id, bot_id, sak=SLACK_API_KEY):
    form_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " + SLACK_API_KEY
    }
    response = requests.get('https://slack.com/api/conversations.members',f'channel={channel_id}',headers=form_headers)
    if response.status_code == 200:
        resp_json = response.json()
        if 'members' in resp_json:
            for member_id in resp_json['members']:
                if member_id == bot_id: return True

    return False

def responder(job,gpt_resp):
    msg = job.message.replace('\n','\n>')[0:300] + '...'
    resp = gpt_resp.replace('\n','\n>')
    return f"*Request:* `{job.id}`\n*<@{job.user_id}> asked:*\n>{msg}\n*GPT Responded:*\n>{resp}"
    #return f"*Request:* `{job.id}`:\n<@{job.user_id}> asked: {job.message}\n*GPT Responded:*\n>{gpt_resp}"

def PrivateDirectMessage(job, gpt_resp):
    global SLACK_API_KEY
    '''payload = {
            "channel": f"{job.user_id}",
            "text": responder(job,gpt_resp)
    }'''
    payload = {
            "channel": f"{job.user_id}",
            "blocks": [
        		{
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": responder(job,gpt_resp)
        			},
        			"accessory": {
        				"type": "button",
        				"text": {
        					"type": "plain_text",
        					"text": "Post to Channel"
        				},
        				"value": f"{job.id}",
        				"action_id": "button-action"
        			}
        		}
        	]
    }
    headers = { "Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + SLACK_API_KEY }

    #return requests.post('https://slack.com/api/chat.postMessage', json=payload, headers=headers)
    response = requests.post(job.webhook_url, json=payload, headers=headers)
    if response.text == 'expired_url':
        return requests.post('https://slack.com/api/chat.postMessage', json=payload, headers=headers)
    else:
        return response

def PrivateMessageInChannel(job, gpt_resp):
    global SLACK_API_KEY
    payload = {
            "channel": f"{job.channel_id}",
            "user": f"{job.user_id}",
            "blocks": [
        		{
        			"type": "section",
        			"text": {
        				"type": "mrkdwn",
        				"text": responder(job,gpt_resp)
        			},
        			"accessory": {
        				"type": "button",
        				"text": {
        					"type": "plain_text",
        					"text": "Post to Channel"
        				},
        				"value": f"{job.id}",
        				"action_id": "button-action"
        			}
        		}
        	]
    }

    headers = { "Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + SLACK_API_KEY }

    return requests.post('https://slack.com/api/chat.postEphemeral', json=payload, headers=headers)

def process_job(job_id):
    print(f"Processing job: {job_id}...", end=" ", flush=True)

    try:

        with Session.begin() as session:
            job = session.query(Job).filter_by(id=job_id).first()
            gpt_response = gpt_chat(job.message) #gpt_complete(job.message)

            if job.channel_id is None or job.channel_id == '':
                response = PrivateDirectMessage(job,gpt_response)
            else:
                c_id = job.channel_id
                if c_id[0] == 'C' and bot_is_member_of_channel(c_id,CHAT_BOT_USER_ID):
                    response = PrivateMessageInChannel(job,gpt_response)
                else:
                    response = PrivateDirectMessage(job,gpt_response)

            if response.status_code == 200:

                with Session.begin() as session:
                    session.query(Job).filter_by(id=job_id).update(
                        {"result": 1, "state": "completed", "response": gpt_response}
                    )

                print(f"{job_id} is complete.")

            else:

                with Session.begin() as session:
                    session.query(Job).filter_by(id=job_id).update(
                        {"result": 0, "state": "failed", "response": "GPT request `{}` failed. Please try again later. Error:{}".format(job_id,response.text) }
                    )

                print(f"{job_id} failed to process.")
                print(f"{response.text}")

                requests.post(SLACK_WEBHOOK_URI, json={ "text": "GPT request `{}` failed. Please try again later. Error: {}".format(job_id,response.text) } )

    except Exception as e:

        with Session.begin() as session:
            session.query(Job).filter_by(id=job_id).update(
                {"result": 0, "state": "failed", "response": e }
            )

        requests.post(SLACK_WEBHOOK_URI, json={ "text": "Unhandled Queue Worker Exception. GPT request `{}` failed. Please try again later. ERROR: {}".format(job_id,str(e)) } )

if __name__ == "__main__":
    print('Waiting for first job...')
    print('Press "Control + C" to halt processing')
    email_subj = 'GPT Slack for VRP Queue Worker Failure'

    try:

        while True:

            if job_id := find_pending_job():
                process_job(job_id)
                print('Waiting for next job...')
                if int(job_id) % 15 == 0: print('Press "Control + C" to halt processing')
            else:
                sleep(1)

    except KeyboardInterrupt:

        send_email(ERROR_SERVICE_SENDER, ERROR_SERVICE_SENDER_TOKEN, ERROR_SERVICE_RECIPIENT, email_subj, 'Script was halted due to keyboard interrupt')

    except Exception as e:

        send_email(ERROR_SERVICE_SENDER, ERROR_SERVICE_SENDER_TOKEN, ERROR_SERVICE_RECIPIENT, email_subj, e)
