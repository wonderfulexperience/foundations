import requests
import time
from pathlib import Path
import os

def send_message(this_message, this_subject, this_API, filename):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox1b96f86f57274a0b85260981f5da32f6.mailgun.org/messages",
        auth=("api", this_API),
        files=[("attachment", (filename, open(filename,"rb").read()))],
        data={"from": "Alexander Trentin <postmaster@sandbox1b96f86f57274a0b85260981f5da32f6.mailgun.org>",
              "to": "Alexander Trentin [redactd]",
               "subject": this_subject,
              "text": this_message})

this_time = time.strftime("%I %p")
this_date = time.strftime("%B %d, %Y")

my_API_mailgun = "[redacted]"
my_filename = "headlines.csv"
my_subject = this_time + " headlines overview. " + this_date
my_message = "Please find attached a file with the headlines of today."
               
my_file = Path(my_filename)
               
if my_file.is_file():
    send_message(my_message, my_subject, my_API_mailgun, my_filename)
    os.remove(my_filename)