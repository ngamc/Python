# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 10:53:47 2018

@author: user
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text  import MIMEText

fromaddr = "python@excalibur.com.hk"
toaddr = "nelsoncheung@excalibur.com.hk"

 
body = """This is a testing message
Please ignore this
"""

def sendm(subject="Checking with you", body=body, to_addr=toaddr):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = to_addr
    msg['Subject'] = subject 
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('192.168.10.28', 25)
    #server.starttls()
    server.login("python", "excpython")
    text = msg.as_string()
    server.sendmail(fromaddr, to_addr, text)
    server.quit()
    
if __name__ == "__main__":
    sendm("Hello There", body )
    