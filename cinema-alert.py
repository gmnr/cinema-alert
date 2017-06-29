#!/usr/bin/python3

# cinema-alert.py
# Created by mini-gui
# Date - June 2017

# A nifty tool to get updates on the O.V. showtimes @ Uci Cinema Bicocca in
# Milan. Complete with a email alert system.

# The program is to be run with a cronjob on the raspberri pi


# Import libraries
import bs4
import yagmail
import requests
import time
import re


# regex def
hours = re.compile(r'\d\d:\d\d')

# yagmail Settings
def send_mail(subject, msg):
    yag = yagmail.SMTP()
    yag.send('your_username@gmail.com', subject, msg)


# the webpage with the showtimes
url = "https://www.ucicinemas.it/cinema/lombardia/milano/uci-cinemas-bicocca-milano/"

# today's date in the correct format
today = time.strftime('%d%m%y')

# define subject for mail alert
subject_alert = 'Cinema Update: {}'.format(time.strftime('%d %B'))

# downloading the page
res = requests.get(url)
try:
    res.raise_for_status()
except Exception as exc:
    subject_prob = 'Problem detected with Update alert of {}'.format(time.strftime('%d %B'))
    msg_prob = 'There was a problem'.format(exc)  # sends an email with the issue
    send_mail(subject_prob, msg_prob)

uci_page = res.content
# saving the BS4 object
soup = bs4.BeautifulSoup(uci_page, 'lxml')

# format of the text div class = showtimes_movies id = movie_ddmmyy
showtimes = soup.find_all(id="movie_{}".format(today))
raw_text = ''

for movie in showtimes:
    raw_text += movie.get_text()

# remove all whitespaces in the page markup
int_list = raw_text.split('\n')
newlist = list(filter(None, int_list))

# format the text from the page
format_msg = ''
for i in range(len(newlist)):
    if hours.search(newlist[i]):
        format_msg += "{}\n".format(newlist[i - 1])
    else:
        format_msg += "{}\n\n".format(newlist[i - 1])

# sort the formatted message
complete_list =format_msg.split('\n\n')
complete_list += [complete_list.pop(0)]
complete_list[-2:] = [''.join(complete_list[-2:])]

# check condition with OV and if positive send mail and hours
for i in range(len(complete_list)):
    if complete_list[i][0:6] == "(O.V.)":
        send_mail(subject_alert, complete_list[i])
