# CableModemLog
This Python 3 script logs the signal quality data from the diagnostic page of a Thomson DCM475 (and maybe other) cable modem.
It will start a new log file every day.  TV and RX stats are logged in separate files.

It is meant to run from cron, Task Scheduler, etc.  

I run it on a Raspberyr Pi with the script and output files ona  NAS share.  Cron runs it every 5 minutes.

Needs Beautiful Soup 4 and Requests for grabbing and interpretting the HTML.

