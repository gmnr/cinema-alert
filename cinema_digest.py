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
from datetime import datetime, timedelta
import re


# regex def
hours = re.compile(r'\d\d:\d\d')


# yagmail send mail
def send_mail(subject, msg):
    yag = yagmail.SMTP()
    yag.send(['recipient'], subject, msg)


# clean the html markup of the day
def format_html(day):
    # format of the text div class = showtimes_movies id = movie_ddmmyy
    showtimes = soup.find_all(id="movie_{}".format(day))
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
    complete_list_day = format_msg.split('\n\n')
    complete_list_day += [complete_list_day.pop(0)]
    complete_list_day[-2:] = [''.join(complete_list_day[-2:])]

    return complete_list_day


# the webpage with the showtimes
url = "https://www.ucicinemas.it/cinema/lombardia/milano/uci-cinemas-bicocca-milano/"


# downloading the page
res = requests.get(url)
try:
    res.raise_for_status()
except Exception as exc:
    subject_prob = 'Problem detected with Update alert of {}'.format(datetime.today().strftime('%d %B'))
    msg_prob = 'There was a problem'.format(exc)  # sends an email with the issue
    send_mail(subject_prob, msg_prob)

uci_page = res.content


# saving the BS4 object
soup = bs4.BeautifulSoup(uci_page, 'lxml')

# create a weekly digest to get updates on the weeks showtimes
digest = ""


# MAIN LOOP
for i in range(0, 7):
    movies_date_format = datetime.today() + timedelta(days=i)
    movies_date = format_html(movies_date_format.strftime('%d%m%y'))
    if any("(O.V.)" in string for string in movies_date):
        digest += '<b>{}</b>\n'.format(movies_date_format.strftime('%d %B'))
    else:
        digest += '<b>{}</b>\nNo movies in original language!\n\n'.format(movies_date_format.strftime('%d %B'))

# check condition with OV and if positive send mail and hours
    for i in range(len(movies_date)):
        if movies_date[i][0:6] == "(O.V.)":
            digest += "{}\n\n".format(movies_date[i])

# create custom subject message
subject = 'Uci Digest Week:  {} - {}'.format(datetime.today().strftime('%d %B'), (datetime.today()+ timedelta(days=6)).strftime('%d %B'))

# send digest email
send_mail(subject, digest)
