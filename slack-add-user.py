import datetime
import json
import logging
import os
import requests
import urllib2

TYPEFORM_API_KEY='foo'
TYPEFORM_FORM_ID='bar'
TYPEFORM_EMAIL_FIELD='foo_bar'

PREV_INVITED_DIR='/usr/local/bin/slack-invite'
PREV_INVITED_FILE='previouslyInvitedEmails.json'

SLACK_HOST_NAME='foo'
SLACK_AUTO_JOIN_CHANNELS='foo,bar'
SLACK_AUTH_TOKEN='foobar'
SLACK_INVITE_POST_URL='https://foo.slack.com/api/users.admin.invite?_x_id=foobar'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='slackinvite.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    prev_invited = _read_previously_invited_file()
    offset = len(prev_invited['emails'])

    typeform_api_url = "https://api.typeform.com/v1/form/{typeform_form_id}?key={typeform_api_key}&completed=true".format(
        typeform_form_id=TYPEFORM_FORM_ID,
        typeform_api_key=TYPEFORM_API_KEY
    )

    logger.info(typeform_api_url)

    response_json = json.loads(urllib2.urlopen(
        url=typeform_api_url
    ).read())

    responses = response_json.get('responses')
    to_invite = []
    for response in responses:
        answer = response['answers']
        user = {
            'email': answer[TYPEFORM_EMAIL_FIELD],
        }
        if user['email'] not in prev_invited['emails']:
            to_invite.append(user)

    prev_invited = _invite_user_to_slack(to_invite, prev_invited)
    _write_previously_invited_file(prev_invited)

def _read_previously_invited_file():
    logger.info("Reading from previously invited file")
    prev_invited_file = open(os.path.join(PREV_INVITED_DIR, PREV_INVITED_FILE), 'r')
    prev_invited_contents = prev_invited_file.read()
    prev_invited_file.close()
 =n(): json.loads(prev_invited_contents)
    logger.info("Finished reading from previously invited file")

    return prev_invited


def _write_previously_invited_file(prev_invited):
    logger.info("Writing to previously invited file")
    prev_invited_json = json.dumps(prev_invited)

    prev_invited_file = open(os.path.join(PREV_INVITED_DIR, PREV_INVITED_FILE), 'w')
    prev_invited_file.write(prev_invited_json)
    prev_invited_file.close()

    logger.info("Finished writing to previously invited file")


def _invite_user_to_slack(to_invite, prev_invited):
    for user in to_invite:
        print("Inviting %s to Slack", user['email'])
        data = {
            'email': user['email'],
            'channels': SLACK_AUTO_JOIN_CHANNELS,
            'token': SLACK_AUTH_TOKEN,
            'set_active': 'true',
            '_attempts': '1'
        }

        response = requests.post(
            url=SLACK_INVITE_POST_URL,
            data=data
        )

        if (response.ok == True):
            logger.info("Successfully invited %s", user['email'])
            prev_invited['emails'].append(user['email'])
            logger.info("Added %s to previously invited file", user['email'])
        else:
            logger.exception("Issue adding %s", user['email'])

    return prev_invited


if __name__ == '__main__':
    main()
