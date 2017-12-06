from twilio.rest import Client
from weather import Weather
import http.client
import json

###########Twilio peferences######################
# Your Account SID from twilio.com/console
account_sid = "AC8d6d1581ea0fe955d771f746799f9645"
# Your Auth Token from twilio.com/console
auth_token  = "9e2c2d603b77981af38250d76b74107c"
# Your Twilio number from which you will send sms
from_number = "+48732483358"
# To which number you want to recieve notifications
to_number = "+48665949288"

###########Yahoo peferences#######################
#Lookup WOEID via http://weather.yahoo.com.
location_id = 63817 #Havana
#for how many days you want to have forecast (more days = more text messages)
how_many_days = 10
#Convert to celsjusz (0 - no, 1 - yes)
conv_far = 1

###########Fotball peferences#######################
#Auth Token
football_token = 'a31ed6dbadff4248a4fedea0a35ea54c'
team_id = '57'

######################################
###########Functions##################
######################################
def check_exist(file_name, to_check): #checking if line exist in file, if no then write it to the file
    try:
        file = open(file_name, 'r')
    except IOError:
        file = open(file_name, 'w')
        file.write(to_check)
        file.close()
        return 0

    for line in file:
        if line == to_check:
            return 1

    file.close()
    file = open(file_name, 'a')
    file.write("\n")
    file.write(to_check)
    file.close()
    return 0

def send_sms(s_body):

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_number,
        from_=from_number,
        body=s_body)
#########################################################
#########################################################

weather = Weather()

location = weather.lookup(location_id)
condition = location.condition()

# Get weather forecasts for the upcoming days.

forecasts = location.forecast()
body2 = "\n"
i = 0
for forecast in forecasts:
    if (i < how_many_days + 1):
        tempmin = int(forecast.low())
        tempmax = int(forecast.high())

        if(conv_far == 1): #convert unit
            tempmin = (tempmin-32)/1.8
            tempmin = round(tempmin, 2)
            tempmax = (tempmax-32)/1.8
            tempmax = round(tempmax, 2)

        body2 = body2 + forecast.date() + " " + forecast.text() + " T:" + str(tempmin) + "->" + str(tempmax) + "\n"
        i = i+1

print(body2)
print(len(body2))
#send_sms(body_2) #sending weather data

string_scores = "\n"

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': football_token, 'X-Response-Control': 'minified' }
connection.request('GET', '/v1/teams/'+ team_id +'/fixtures?timeFrame=p7', None, headers )
response = json.loads(connection.getresponse().read().decode())
fixtures = response["fixtures"]
for fixture in fixtures:
    string_match = fixture["date"] + " - " + fixture["homeTeamName"] + " " + str(fixture["result"]["goalsHomeTeam"]) + " : " + str(fixture["result"]["goalsAwayTeam"]) + " " + fixture["awayTeamName"]
    if check_exist("scores.txt", string_match+"\n") == 0:
        string_scores = string_scores + string_match + "\n"
    print(string_match)

if len(string_scores) > 5: #checking if some scores are waiting for send
    #send_sms(string_scores)#sending data through sms
    print("Wyslano smsa")

#print (response)
print(string_scores)

#print(match)