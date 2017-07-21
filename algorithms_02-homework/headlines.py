from bs4 import BeautifulSoup
import requests
import time
import csv

#scraping Swiss news website 20min.ch
response = requests.get("https://www.20min.ch")
doc = BeautifulSoup(response.text,"html.parser")

#first ten headlines
headlines = doc.find_all("h2")[:10]

headlines_message = ""
headlines_list = []

for headline in headlines:
    headline_list = []
    headline_text = headline.text
    headline_sub = headline.find_previous("h3").text
    headline_summary = headline.find_next("p").text
    headline_link = "http://www.20min.ch"+headline.find("a")['href']
    this_headline = headline_text+"\n"+headline_sub+"\n"+headline_summary+"\n"+headline_link
    headlines_message += this_headline + "\n\n"
    headline_list = [headline_text,headline_sub,headline_summary,headline_link]
    headlines_list.append(headline_list)

#append the CSV to be sent at the end of the day (another Python script will send it out and delete it)
with open("headlines.csv", "a") as f:
      writer = csv.writer(f)
      writer.writerows(headlines_list)

#send the message
def send_message(this_message, this_subject, this_API):
    return requests.post(
        "https://api.mailgun.net/v3/[redacted]/messages",
        auth=("api", this_API),
        data={"from": "[redacted]",
              "to": "[redacted]",
              "subject": this_subject,
              "text": this_message})

this_time = time.strftime("%I %p")
this_date = time.strftime("%B %d, %Y")

my_API_mailgun = "[redacted]"
my_subject = this_time + " news summary. " + this_date
my_message = headlines_message
send_message(my_message, my_subject, my_API_mailgun)
