# Typeform to Slack Integration Script

## OVERVIEW
Following this tutorial, a script was written to automatically retrieve emails from Typeform form and auto-inviting to an organization's Slack.

## TECHNICAL DETAILS
### PreRequisites
An Auth Token associated with an admin Slack account needed to be created.  The admin account control was handed over to Zach and David.   You need to generate an auth token for that account

### Script
The following values need to be changed for a specific application
```
TYPEFORM_API_KEY
TYPEFORM_FORM_ID
TYPEFORM_EMAIL_FIELD

SLACK_HOST_NAME
SLACK_AUTO_JOIN_CHANNELS
SLACK_AUTH_TOKEN
SLACK_INVITE_POST_URL
```
By default the script should be located and run from /usr/local/bin/slack-invite/slack-add-user.py.
The script also uses a file where it stores previously invited emails.  It is located at /usr/local/bin/slack-invite/previouslyInvitedEmails.json

The script logic follows:
1. Read previouslyInvitedEmails.json and load into memory
2. Read from the Typeform API to get all the responses
3. Iterate through the responses and parse out the emails and verify that it was not previously invited
4. If not previously invited, add them to a list of people to invite
5. Invite all the users in the list of emails to invite through the Slack API
6. If we successfully invite them, add the user to the previously invited list
7. Store the new list of previously invited emails to previouslyInvitedEmails.json

### Running the Script
A Cron job can be added to run the script every 10 minutes
1. Run the command `crontab -e`
2. Add the following line to the bottom of the file
```
*/10 * * * * python /usr/local/bin/slack-invite/slack-add-user.py >> /usr/local/bin/slackinvite.log 2>&1
```

### API References
Typeform’s Response API
Slack's API
