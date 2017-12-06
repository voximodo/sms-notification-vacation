from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "sid"
# Your Auth Token from twilio.com/console
auth_token  = "auth"

from_number = ""

def conf_twilio(a_sid, a_token, f_number):
    auth_token = a_token
    account_sid = a_sid
    from_number = f_number

def send_sms(a_sid, a_token, f_number, t_number, s_body):

    client = Client(a_sid, a_token)

    message = client.messages.create(
        to=t_number,
        from_=f_number,
        body=s_body)