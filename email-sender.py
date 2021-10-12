import smtplib
from dotenv import load_dotenv
import os

def send_email(eml_file, type):
    smtp = None
    with open(eml_file) as f:
        message = f.read()
    try:
        if type == "hotmail":
            smtp = smtplib.SMTP('smtp.live.com', 587)
            smtp.ehlo()
            smtp.starttls()
            # I forgot I am going to zip up this folder and send it over so storing passwords in a .env doesn't hide it.
            # Login Details stored in .env
            smtp.login(os.environ.get('hotmail'), os.environ.get('h_password'))
            smtp.sendmail('sleepyboy123@hotmail.com', 'sleepyboi234@hotmail.com', message)
            print('Sent to Hotmail.')
        if type == "gmail":
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.ehlo()
            # Login Details stored in .env
            smtp.login(os.environ.get('gmail'), os.environ.get('g_password'))
            smtp.sendmail('sleepytesting12345@gmail.com', 'sleepyboi1234@gmail.com', message)
            print('Sent to Gmail.')
    except Exception as e:
        print('Failed to Send Mail.')
        print(str(e))
    finally:
        if smtp != None:
            smtp.close()

if __name__ == "__main__":
    load_dotenv()
    send_email('hotmail_phishing.eml', 'hotmail')
    send_email('google_phishing.eml', 'gmail')
    
