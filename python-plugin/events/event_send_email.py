# Task: On the NEW-DATA-PACKET event, send an email through an SMTP server when the packet contains " 911". The same idea works for any text that must trigger a message.
# Input: Event parameters with DATA_PACKET.
# Output: An email with the event context.
# Product: AGG data loggers with the Python plugin (plugin.py API)
# Source: AGG Software, Python plugin samples
# License: MIT, see LICENSE in the repository root

# This example handles the "NEW-DATA-PACKET" event, analyzes its content, and
# sends an email

from plugin import *
import smtplib, ssl
from email.message import EmailMessage

plugin_name = 'Test plugin'
send_count = 0

# this example uses the GMail SMTP server
smtp_host = 'smtp.gmail.com'
smtp_port = 465
smtp_login = 'test1@gmail.com'
smtp_pass = 'mypassword'

sender_email = smtp_login
receiver_email = 'test2@gmail.com'

def main():
    global plugin_name

    print('Loaded: ' + plugin_name)

def FilterData(callparams, datasource, datain, dataout):
    # do nothing
    pass

# event_params - list with all event parameters (depends on the event)
# datasource - data source ID (can be None)
# event - event name

def EventData(event_params, datasource, event):
    global send_count

    print('Event: ' + str(event))

    if event == 'NEW-DATA-PACKET':

        # get the necessary value from the event context (parameters)
        data = event_params.ItemValueByName('DATA_PACKET')
        if data is None:
            return

        # check the presence of the important value
        if data.find(' 911') < 0:
            return

        print("Sending email")
        send_count += 1

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            try:
                print("Sending HELLO")
                server.ehlo() # Can be omitted
                print("Securing connection")
                # server.starttls(context=context) # Secure the connection
                print("Signing in")
                server.login(smtp_login, smtp_pass)

                # sends the plain text message
                body = 'Event received: ' + event + '\n'
                if event_params.Count > 0:
                    body = ' Event context:\n'
                    for idx in range(event_params.Count):
                        item = event_params.Items[idx]
                        body = body  + '  ' + item.Name + '=' + str(item.Value) + '\n'

                message = EmailMessage()
                message.set_content(body)

                message['Subject'] = 'Event ' + event
                message['From'] = sender_email
                message['To'] = receiver_email

                print("Sending email body")
                server.send_message(message)
                print("Sent successfully")

            except Exception as error:
                print('Unable to send an email: {0}'.format(error))
            finally:
                server.quit()

    else:
        print('Another event: ' + event)


def ParseData(callparams, datasource, buffer, dataout):
    # do nothing
    pass

def ExportData(callparams, datasource, datain):
    # do nothing
    pass

main()