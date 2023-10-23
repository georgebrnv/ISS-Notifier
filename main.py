import requests
from datetime import datetime
import smtplib
import time

MY_LNG = -70.8430827
MY_LAT = 25.2272086

MY_LOGIN = "example@email.ru"
MY_PASSWORD = "password123"

now = datetime.now()


def iss_above_me():
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True
    return False


def send_email():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=MY_LOGIN, password=MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_LOGIN,
        to_addrs=MY_LOGIN,
        msg=f"Subject: Look up!\n\nISS is above you in the sky!"
    )
    connection.close()


# ISS
iss_data_response = requests.get(url="http://api.open-notify.org/iss-now.json")
data = iss_data_response.json()

iss_longitude = float(data["iss_position"]["longitude"])
iss_latitude = float(data["iss_position"]["latitude"])

iss_position = (iss_longitude, iss_latitude)


# Check if it's a night time
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    sun_data = sun_response.json()

    sunrise_hour = int(sun_data["results"]["sunrise"].split('T')[1].split(':')[0])
    sunset_hour = int(sun_data["results"]["sunset"].split('T')[1].split(':')[0])

    if sunset_hour <= now.hour <= sunrise_hour:
        return True
    return False


# Continuously executing code and check (every 60 seconds) whenever ISS is above you
# and it's a nighttime to send an email
while True:
    time.sleep(60)
    if is_night() and iss_above_me():
        send_email()
