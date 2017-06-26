#!/usr/bin/python3

# cinema-alert.py
# Created by mini-gui
# Date -June 2017

# A nifty tool to get updates on the O.V. showtimes @ Uci Cinema Bicocca in
# Milan. Complete with a email alert system.

# The program is to be run with a cronjob on the raspberri pi


# Import libraries
import bs4
import yagmail
import requests
import time


# the webpage with the showtimes
url = "https://www.ucicinemas.it/cinema/lombardia/milano/uci-cinemas-bicocca-milano/"

# today's date in the correct format
today = time.strftime('%d%m%y')

# create an empty dictionary that will contain the movie title
uci_movies = {}

# downloading the page
res = requests.get(url)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem'.format(exc))  # to be written in the log eventually
uci_page = res.content

# saving the BS4 object
soup = bs4.BeautifulSoup(uci_page)

# format of the text div class = showtimes_movies id = movie_ddmmyy
showtimes = soup.find_all(id="movie_{}".format(today))

raw_text = ''

for movie in showtimes:
    raw_text += movie.get_text()


# yagmail Settings
yag = yagmail.SMTP()
yag.send('your_username@gmail.com', 'Cinema Update: {}'.format(today), raw_text)
