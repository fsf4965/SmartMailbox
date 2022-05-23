import LCD1602
import time
import smtplib
import RPi.GPIO as GPIO

TO= "USER MAIL ADDRESS HERE" #all of the credentials
GMAIL_USER="SMART MAILBOX MAIL ADDRESS HERE"
PASS= 'SMART MAILBOX MAIL PASSWORD HERE'

SUBJECT = 'Mail Alert!'
TEXT = 'You have received new mail(s) in your mailbox!'

ObstaclePin = 11

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    LCD1602.init(0x27, 1)   # init(slave address, background light)
    LCD1602.write(0, 0, 'Mailbox status:')
    LCD1602.write(1, 1, 'Launching...')
    time.sleep(5)
    
def sendmail_loop():
    mailbox_status = 'Mailbox status:'
    mailbox_full = 'Full             '
    mailbox_empty = 'Empty.           '
    
    while True:
        if (0 == GPIO.input(ObstaclePin)):
            LCD1602.write(0, 0, mailbox_status)
            LCD1602.write(1, 1, mailbox_full)
            
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
            LCD1602.write(0, 0, mailbox_status)
            LCD1602.write(1, 1, mailbox_empty)
            
def destroy():
    GPIO.cleanup() 
    
if __name__ == '__main__':     # Program start from here
    setup()
    try:
        sendmail_loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()