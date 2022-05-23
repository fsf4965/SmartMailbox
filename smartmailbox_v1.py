import time
import smtplib
import RPi.GPIO as GPIO

TO= "fsf4965@gmail.com" #all of the credentials
GMAIL_USER="comp816.smartmailbox@gmail.com"
PASS= 'baZuD29aPbRcdhT'

SUBJECT = 'Mail Alert!'
TEXT = 'You have received new mail(s) in your mailbox!'

ObstaclePin = 11

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def sendmail_loop():
    while True:
        if (0 == GPIO.input(ObstaclePin)):
            print("Sending text")
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(GMAIL_USER,PASS)
            header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
            header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
            print(header)
            msg = header + '\n' + TEXT + '\n\n'
            server.sendmail(GMAIL_USER,TO,msg)
            server.quit()
            time.sleep(1)
            print("Text sent")
            time.sleep(60*2)
        else:
            time.sleep(5)
            
def destroy():
    GPIO.cleanup() 
    
if __name__ == '__main__':     # Program start from here
    setup()
    try:
        sendmail_loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
