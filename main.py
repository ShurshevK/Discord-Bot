import discord 
import os 
from dotenv import load_dotenv 
import json
import pandas_datareader as web
from neuralintents import GenericAssistant
from weather import *
import requests


chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()



client = discord.Client()





load_dotenv()
TOKEN = os.getenv("TOKEN")
api_key = os.getenv("API")

def get_stock_price(ticker):
    data = web.DataReader(ticker, "yahoo")
    return data["Close"].iloc[-1]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hi, this is Bair, Alex and Kirill BOT!")

    if message.content == "$private":
        await message.author.send("Hello in private Brother")

    if message.content.startswith("$stockprice"):
        if len(message.content.split(" ")) == 2:
            ticker = message.content.split(" ")[1]
            price = get_stock_price(ticker)
            await message.channel.send(f"Stock price of {ticker} is {price} ")
    
    if message.content.startswith("$aibot"):
        respond = chatbot.request(message.content[7:])
        await message.channel.send(respond)

    if message.content.startswith("$weather"):
        if len(message.content.split(" ")) == 2:
            location = message.content.split(" ")[1]
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))
    


@client.event
async def on_connect():
    print("Bot connected to the server!")
    
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Welcome to the server {member}!")   



client.run(TOKEN)    
