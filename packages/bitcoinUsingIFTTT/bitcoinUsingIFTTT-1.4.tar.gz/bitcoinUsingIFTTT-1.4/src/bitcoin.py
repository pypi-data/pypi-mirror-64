import requests


def link_telegram():
    def _end():
        print('Server has encountered error ! ')
    try:
        print('''
    Requirements :
    1 - IFTTT Account.
    2 - Applet created with webhooks and telgram services.
    3 - Two event for emergency alert and normal alerts.
    3 - Suggested Message Format is
    Normal Alert : {Bitcoin Alerts : <br> value1 }
    Emergency Alert : {Emergency Alert : <br> value1}
    ''')

        country = input(
            'Enter the country code to setup your telgram alerts : ')
        thresh = float(input('Enter Emergency Threshold : '))
        event = input('Enter the event name that you created in IFTTT : ')
        threshevent = input('Enter the Emergency threshold event Name : ')
        ifttt_TOKEN = input("Enter the IFTTT token ,You Got from Webhooks : ")
        timer = int(
            input('''Enter interval time for alerts
            NOTE use 720 for 1hr interval : '''))
        from time import sleep
        print('Your Project is getting created !!!')
        sleep(5)
        print('IFTTT is linked.')
    except Exception:
        print("Input is invalid !")
        _end()

    def get_data(country):
        try:
            connection = requests.get(url='https://blockchain.info/ticker')
            data_in__json = connection.json()
            return (str(data_in__json[country.upper()]['last']) +
                    ' ' + str(data_in__json[country.upper()]['symbol']))
        except Exception:
            print('Data is not accessable from the url provided.')

    from datetime import datetime
    from pytz import timezone

    def formatdata():
        try:
            data = get_data(country)
            format = "Date: %Y-%m-%d || Time: %H:%M:%S"
            now_utc = datetime.now(timezone('UTC'))
            now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
            time = (now_asia.strftime(format))
            return (f'Price : {data} <br>{time} <br> <br> ')
        except Exception:
            print("Problem occured in formatting !")

    from time import sleep
    import requests

    def sendtoIFTTT():
        datahistory = []
        i = 1
        # infinite loop is created as new bitcoin price uodates keep coming
        while True:
            # data variable is used to stored data recieved from formatdata
            # module.
            data = formatdata()
            # everytime a data is collected it is added to the list.

            try:
                com = float(data.split(" ")[2])
                if com < int(thresh):
                    price = com
                    symbol = (data.split(' ')[3])
                    string = f'{price} {symbol}'
                    requests.post(
                        url=f'https://maker.ifttt.com/trigger/{threshevent}/with/key/{ifttt_TOKEN}',
                        json={
                            'value1': (string)})
                    print('Posted Emergency Alert!')
                else:
                    datahistory.append(data)
            except Exception:
                print('Entered Wrong Details!')
            try:
                print(f'Data collected {i} times !')
                # incrementing the i variable after every loop
                i += 1
                # time is set here (seconds)!
                sleep(timer)
                # this is the IFTTT Token recieved from IFTTT services
                ifttt_url = f'https://maker.ifttt.com/trigger/{event}/with/key/{ifttt_TOKEN}'
            except Exception:
                print("Project is not setupp Properly !")
            if len(datahistory) == 5:
                try:

                    # the data in list is add to string module .
                    string = "".join([x + '\n' for x in datahistory])

                    # value1 is the datafield we provided in IFTTT applet so we
                    # are assigning our string to it
                    data = {'value1': (string)}
                    # session is opened to start posting
                    s = requests.session()
                    # url and and data is send as json
                    requests.post(ifttt_url, json=data)
                    print(f'\nsent ! ')
                    # session is closed immediatelt after data is posted.
                    s.close
                    # collected data is deleted
                    del data
                    # list is cleared to get new data in the new session
                    datahistory = []

                    print('Starting New Session !')
                    # again new sesssion is started
                    sendtoIFTTT()

                except Exception:
                    print('something went wrong !!')
                    sendtoIFTTT()

    def main():
        from time import sleep
        from tqdm import tqdm
        import sys
        try:
            animation = "✒✔༼ つ ◕_◕ ༽つ|/-\\"
            for i in range(25):
                sleep(0.1)
                sys.stdout.write("\r" + animation[i % len(animation)])
                sys.stdout.flush()
            print("""
      ----------------------------------------------
      ----------------------------------------------
      ---------   BITCOIN ALERT SERVER   -----------
      ----------------------------------------------
      ----------------------------------------------
      """)
            print('''
      Available Country :
      INR - INDIA
      USD - UNITED STATES OF AMERICA
      JPY - JAPAN
      EUR - EUROPE
      AND Still more !
      ''')
            # this module is imported to run the whole code and
            # hide the all other working procedure to avoid
            # modifications form others.
            # Starting the server !
            loop = tqdm(total=100, position=0, leave=False)
            for k in range(100):
                loop.set_description("Starting the Server ! ")
                sleep(.1)
                loop.update(1)
            loop.close()
            choice = input('Do you want to Start getting alert y/n: ')
            if choice == 'y':
                sendtoIFTTT()
            else:
                print('See you later !!')
        except(Exception):
            print('Starting the Project !')
            sendtoIFTTT()
    main()


def getPrice():
    country = input('Enter the country code : ')
    try:
        connection = requests.get(url='https://blockchain.info/ticker')
        data_in__json = connection.json()
        print(str(data_in__json[country.upper()]['last']) +
              ' ' + str(data_in__json[country.upper()]['symbol']))
    except Exception:
        print('Data is not accessable from the url provided.')


def joinChannel():
    name = input("Enter your name : ")
    print(
        f'''Welcome {name.capitalize()}  use this link
        : \'http://t.me/praveenNagaraj\'''')
