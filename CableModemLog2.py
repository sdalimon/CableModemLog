#! /usr/bin/python3

### Scrape the signal level logs from a Thomson cable modem
# Shawn D'Alimonte
# This is public domain

import requests
import bs4
from datetime import datetime
from datetime import date
from os.path import exists

url = 'http://192.168.100.1/Diagnostics.asp'
rx_log_file = date.today().strftime('%Y%m%d')+'_rx_log.txt'
tx_log_file = date.today().strftime('%Y%m%d')+'_tx_log.txt'

# Get the stats page from the modem
res = requests.get(url)
res.raise_for_status()

# Get current time for the log file
currentTime = datetime.now()
currentTimeStr = currentTime.strftime('%Y-%m-%d %H:%M:%S')
#print(currentTimeStr)

# Temp dump the file to examine in browser
#f = open('modem_diag.html', 'wb')
#for x in res.iter_content():
#    f.write(x)
#f.close()

# If the log files don't exist, create them and add the header lines
if not exists(rx_log_file):
    f = open(rx_log_file, 'w')
    print('Time', 'Ch', 'Freq', 'Pwr', 'SNR', 'BER', sep='\t', file=f)
    f.close()
if not exists(tx_log_file):
    f = open(tx_log_file, 'w')
    print('Time', 'Ch', 'Freq', 'Pwr', sep='\t', file=f)
    f.close()
    


soup = bs4.BeautifulSoup(res.text, 'html.parser')

# Rx Stats are the first table with CSS class 'light'
# table is:
# Channel, Frequency, Power, SNR, BER, Modulation
# skip the first line since it is headings
rx_table = soup.find_all('table', class_='light')[0]
f = open(rx_log_file, 'a')
for line in rx_table.findAll('tr')[1:]:
    stats=line.findAll('td')
    ch = stats[0].getText()
    freq = stats[1].getText()
    power = stats[2].getText()
    snr = stats[3].getText()
    ber = stats[4].getText()
    mod = stats[5].getText()
    print(currentTimeStr, ch, freq, power, snr, ber, sep='\t', file=f)
f.close()

# Tx Stats are the second table with CSS class 'light'
# table is:
# Channel, Frequency, Power, Modulation
# skip the first line since it is headings
tx_table = soup.find_all('table', class_='light')[1]
f = open(tx_log_file, 'a')
for line in tx_table.findAll('tr')[1:]:
    stats=line.findAll('td')
    ch = stats[0].getText()
    freq = stats[1].getText()
    power = stats[2].getText()
    mod = stats[3].getText()
    print(currentTimeStr, ch, freq, power, sep='\t', file=f)
f.close()
