BitCoin Notifier:

Working Procedure: 

Installation
Following command on terminal will install bitcoin_karishma package/module from PIP

pip3 install bitcoin_karishma
Following command on terminal will install the latest bitcoin_karishma package/module from PIP

pip3 install -U bitcoin_karishma

Usage

Following query on terminal will provide you with all the help options available

Input :

bitcoin-notifier -h

Output :

usage: bitcoin-notifier [-h] [-i interval] [-t threshold]
Bitcoin Notifier
optional arguments:
  -h, --help            show this help message and exit
  -i interval, --interval interval
                        Time interval in minutes
  -t threshold, --threshold threshold
                        Threshold in USD
Following query on terminal will provide you five prices of Bitcoin at a time at one min interval and whenever it falls below $10000 and emergency notification will be sent.

bitcoin-notifier -i 1 -t 10000

Un-installation:

Following command on terminal will uninstall bitcoin-notifier package/module from your device

pip3 uninstall bitcoin_karishma

• The Project is divided into four functions/modules:

 get_latest_price() – Here I have used request module to collect data from source(‘blockchain.com’), Once it gets data it will convert the data into json format which is returned back to the function.

 post_ifttt_webhook() – Here the formatted data is sent to users as notifications once it acquires data from previous module.

 format_bitcoin_history() - The main objective of this module is to format the notification message which will be sent to users.

 main() – Here it will integrate all the steps and sets up timer to repeat the process at certain intervals.

• IFTTT Applets:

 Webhooks, Telegram, Notifications, Email and Android SMS services are used here.

 When an event 'bitcoin_price_emergency is occurred in the webhooks it will send the event value to Notification in your phone and an email is sent to the email listed in the service.

 When and event 'bitcoin_price_update is occurred in the webhooks it will send the event value to the Telegram Channel 'Bitcoin Notifier' and text message to the phone number linked to the service.

Credentials:  Webhooks Key- eA_ZN_ZsBcX4FZmsgzdc_7_yppNdLzDCWsJaoAz65Ci

 Telegram Channel Link- (@bitcoin_notifier)https://t.me/Bitcoin_update_21

 Email linked to the service- karishmaag21@gmail.com

 Phone Number linked to the service- +917738222219