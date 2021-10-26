import requests as req
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

# Open log file
logFile = open("logs.txt", "a")

# GET data
try:
    TargetDisneyBabyUrl = "https://ac.cnstrc.com/browse/brandcode/disney?c=ciojs-client-2.8.4&key=key_kWcXakjuyHSxpu75&i=2be81c87-0f59-40ce-bf17-b24ca7153c32&s=1&ef-constructorio=&us=web&ui=nosessionid&page=1&num_results_per_page=96&filters%5Bgroup_id%5D=W93741&sort_by=price&sort_order=ascending&_dt=1635258936084"
except Exception as e:
    logFile.write(f'{date.today().strftime("%B %d")} - {str(e)}\n')

try:
    TargetBabyClearanceUrl = "https://ac.cnstrc.com/browse/group_id/W677760?c=ciojs-client-2.8.4&key=key_kWcXakjuyHSxpu75&i=2be81c87-0f59-40ce-bf17-b24ca7153c32&s=1&ef-constructorio=&us=web&ui=nosessionid&page=1&num_results_per_page=96&sort_by=price&sort_order=ascending&_dt=1635260075314"
except Exception as e:
    logFile.write(f'{date.today().strftime("%B %d")} - {str(e)}\n')

# Items list
itemsUnder5Map = []
# Response Data
disneyResponse = req.get(TargetDisneyBabyUrl)
disneyData = disneyResponse.json()
babyResponse = req.get(TargetBabyClearanceUrl)
babyData = babyResponse.json()
# JSON Items
disneyItems = disneyData["response"]["results"]
babyItems = babyData["response"]["results"]

# Struct dict data and push to arrays
for item in disneyItems:
    if int(item["data"]["price"]) <= 5:
        itemsUnder5Map.append(
            {"name": item["value"],
             "url": item["data"]["baseproducturl"],
             "price": item["data"]["price"],
             "img": item["data"]["image_url"]
             })

for item in babyItems:
    if int(item["data"]["price"]) <= 5:
        itemsUnder5Map.append(
            {"name": item["value"],
             "url": item["data"]["baseproducturl"],
             "price": item["data"]["price"],
             "img": item["data"]["image_url"]
             })


# Structure email components
port = 587
smtp_server = "smtp.gmail.com"
sendEmail = "benbabyitems@gmail.com"
receiveEmail = "bendotwhitely@gmail.com"
password = "Jessie12212!"
message = MIMEMultipart("alternative")
message["Subject"] = "Baby Items For " + date.today().strftime("%B %d")
message["From"] = sendEmail
message["To"] = receiveEmail

# Build HTML
htmlBuilder = ""
for i in itemsUnder5Map:
    htmlBuilder = htmlBuilder + \
        f'<li><a href="{i.get("url")}">{i.get("name")} - ${int(i.get("price"))}</a><img src="{i.get("img")}" alt="{i.get("url")} image" width="150px" height="150px"</li></br>'

html = f"""\
<html>
    <body>
        <ul>
            {htmlBuilder}
        </ul>
    </body>
</html> 
"""

part = MIMEText(html, "html")
message.attach(part)

# Create a secure SSL context
context = ssl.create_default_context()
# Try to send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sendEmail, password)
    server.sendmail(sendEmail, receiveEmail, message.as_string())
except Exception as e:
    logFile.write(f'{date.today().strftime("%B %d")} - {str(e)}\n')
finally:
    server.quit()
    logFile.close()

print('complete')
