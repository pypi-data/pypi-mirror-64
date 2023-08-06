import requests
import time
from datetime import datetime

# Notification function if bitcoin price falls from given lower bound.
def emergency(value):
    data = {"value1":value}
    requests.post('https://maker.ifttt.com/trigger/emergency_message/with/key/jQMPZa_jNCtD7FIGhD9uohInvAIVB7-_XI1H_GCh2xD', json=data)

#Notification function if bitcoin price cross the upper bound
def bounce(value):
    data = {"value1":value}
    requests.post('https://maker.ifttt.com/trigger/bounce/with/key/jQMPZa_jNCtD7FIGhD9uohInvAIVB7-_XI1H_GCh2xD', json=data)

# Regular updating of price of bitcoin.
def update(price_list):
    price_list = "<br>".join(price_list)
    data = {"value1":price_list}
    requests.post('https://maker.ifttt.com/trigger/bitcoin_price/with/key/jQMPZa_jNCtD7FIGhD9uohInvAIVB7-_XI1H_GCh2xD', json=data)

# Function for taking price of bitcoin from API. 
def getting_price():
    response = (requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')).json()
    value = response['bpi']['USD']['rate']
    value = float(value.replace(",",""))
    date_time = datetime.now().strftime("%D %H:%M")
    return [date_time, value]

# Function for governing all type of notifications.
def notify(Lower_bound, Upper_bound):
    # Two variable for keeping time of last notifiaction of out of range price.
    time_lower = 0
    time_upper = 0
    count1 = 0
    count2 = 0
    price_list = []   #For saving 5 prices of bitcoin of different time.
    # Infinte Loop
    while True:
        price = getting_price()   # For getting price of bitcoin, function will return a list [price, time].

        if price[1]<Lower_bound and Lower_bound!=0: # Checking if price is lower than lower bound and if user set the lower bound or not.
            price[1] = "<i>{}</i>".format(price[1])   # The price of bitcoin will shows in Italic.

            if count1 == 0 or time_lower>=3600:   #If time for last calling of emergency function is more than or equal to 1 hour, it will call again.
                emergency(price[1])
                count1=1
                time_lower = 0    # Setting time again to 0. 

        elif price[1]>Upper_bound and Upper_bound!=0:   # Checking if price is more than upper bound and if user set upper bound or not.
            price[1] = "<b>{}</b>".format(price[1])   # The price of bitcoin will shows in Bold.

            if count2 == 0 or time_upper>=3600:   #If time for last calling of bounce function is more than or equal to 1 hour, it will call again.
                bounce(price[1])
                count2 = 1
                time_upper = 0    #   Setting time again to 0.

        price = "{}: ${}".format(price[0], price[1]) # Making format in "Date Time: $Price".
        price_list.append(price)
        if len(price_list)>=5:  # If we get 5 values then we will call update function.
            update(price_list)
            price_list = []   # Emptying List.

        # keeping track of time.
        time_lower+=60*5    
        time_upper+=60*5
        time.sleep(60*5)    # Stoping program for 5 minutes

# We are taking upper and lower bound so chceking if lower bound is lower than upper bound or not.
def main():
    reply = "Y"
    while reply == "Y":
        Lower_bound = int(input("Enter Lower Bound of price(if you do not want to set this enter 0):"))
        Upper_bound = int(input("Enter Upper Bound of Price(if you do not want to set this enter 0):"))
    
        if Lower_bound>Upper_bound and Upper_bound!=0:
            print("Lower Bound should be lower than Upper Bound.")
            reply = input("If you want to correct this enter Y or for exit N:")
        else:
            notify(Lower_bound, Upper_bound)
            break

if __name__=="__main__":
    main()