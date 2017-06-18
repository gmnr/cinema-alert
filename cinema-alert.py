#!/usr/bin/python3

# cinema-alert.py
# Created by Guido Minieri
# Date -June 2017

# A nifty tool to get updates on the O.V. showtimes @ Uci Cinema Bicocca in
# Milan. Complete with a email alert system.

# The program is to be run with a cronjob on the raspberri pi


# libraries import
import datetime
import bs4
import smtplib
import requests


'''
1. Navigate to the Cinema site
2. Download the page with BS4
3. Select today's date with the div id = movie_ddmmyy
4. Iterate through a list of nested html elements
    a. get name from span class = movie_name
    b. get list of showtimes from ul class = showtime__movie__shows
5. Get only the names that start with "(O.V.)"
6. Store results in the email body to be sent after a while
'''
