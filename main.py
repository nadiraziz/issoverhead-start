import time
import requests
from datetime import datetime
import smtplib
# Your latitude
MY_LAT = 11.684956
# Your longitude
MY_LONG = 75.553613

MY_MAIL = "nadirtest7@gmail.com"
PASSWORD = "Nadir@123"


def is_iss_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour_now = time_now.hour
    if sunset <= hour_now or sunrise >= hour_now:
        return True


while True:
    time.sleep(60)
    if is_iss_near() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_MAIL,
                to_addrs="nadiraziziyah@gmail.com",
                msg="Subject: iss is near to us\n\n LOOK UP")
