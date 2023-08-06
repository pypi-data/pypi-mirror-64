from tqdm import tqdm
from time import sleep
import requests

def getPrice():
    country=input('Enter the Country Code : ').upper()
    connect = requests.get(url='https://blockchain.info/ticker')
    data = connect.json()
    loop = tqdm(total = 100,position = 0 ,leave = False)
    for k in range(100):
      loop.set_description("Getting Latest Price ")
      sleep(.01)
      loop.update(1)
    loop.close()
    return ('The Current Bitcoin Price is : '+str(data[country]['last'])+ ' ' + str(data[country]['symbol']))

def joinchannel():
  return ('Join this Link  http://t.me/praveenNagaraj to get \nTelegram Updates regularly Every Hour')
joinchannel()