# -*- coding: utf-8 -*-
"""TELEbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1puOA_5bue8TVyZc-J6p6pySOkdpy5RTY

Detect and reply message
"""

import json
import requests
from requests import Session


def print_data(request):
  c_url="https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
  c_parameters = {
    'convert' : 'INR'
  }
  headers={
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '5aae8aea-fa41-43b7-b65a-0bddea0fbc86'
  }
  session=Session()
  session.headers.update(headers)

  response=session.get(c_url,params=c_parameters)
  Data=json.loads(response.text)["data"]
  ind=-1
  for res in Data:
    if request.lower() == res["name"].lower() or request.lower() == res["symbol"].lower():
      ind= Data.index(res)

  c_price=(json.loads(response.text)["data"][ind]["quote"]["INR"]["price"])
  percent_change_24h = (json.loads(response.text)["data"][ind]["quote"]["INR"]["percent_change_24h"])
  percent_change_1w = (json.loads(response.text)["data"][ind]["quote"]["INR"]["percent_change_7d"])
  percent_change_30d = (json.loads(response.text)["data"][ind]["quote"]["INR"]["percent_change_30d"])
  percent_change_1h = (json.loads(response.text)["data"][ind]["quote"]["INR"]["percent_change_1h"])
  coin_n= (json.loads(response.text)["data"][ind]["name"])
  coin_s= (json.loads(response.text)["data"][ind]["symbol"])
  s=""
  if request=="welcome":
    return "Welcome to the cryptoBOT world!"
  # elif coin=="hi" or "hello" or "hii" or "hlo" or "Hello" or "Hi":
  #   return "Hello! Enter coin to know its latest price."
  elif ind == -1:
    return "No coin found! I'm still learning..."

  s=  coin_s+ "  :" +" "*50+"Price:  " +u"\u20B9"+ str(round(c_price, 4))+" "*30+  "24H%:   "+ str(round(percent_change_24h, 4))+" "*40+ "7d:  "+str(round(percent_change_1w, 4))

  return s

base_url="https://api.telegram.org/bot5479441757:AAHDUKdGvDAZAF2FWUCLwf4nZDqG4OyXK_g"


def read_msg(offset):
  parameters={ 
    "offset" : offset
  }
  
    
  resp =    requests.get(base_url + "/getUpdates",data=parameters)
  data=resp.json()

  for result in data["result"]:
    send_msg(result)
  
  if data["result"]:
    return data["result"][-1]["update_id"] + 1

def send_msg(coin):
  if 'message' in coin:
    if 'text' in coin["message"]:
      text = coin["message"]["text"]
    else:
      text= "welcome"
  else:
    text="welcome"
  
  message_id = coin["message"]["message_id"]
  parameters={ 
      "chat_id" : "-710842744",
      "text" : print_data(text)
  } 
  resp=requests.get(base_url + "/sendMessage",parameters)
  print(resp.text)




offset=0
while True:
  offset=read_msg(offset)
