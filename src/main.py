import os
import sys
import json
import time
import math
import discord
import aiohttp
import asyncio

MESSAGE_PREFIX     = os.getenv('MESSAGE_PREFIX')
DISCORD_BOT_TOKEN  = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
DISCORD_MESSAGE_ID = int(os.getenv('DISCORD_MESSAGE_ID'))
NEOS_USERNAME      = os.getenv('NEOS_USERNAME')
NEOS_PASSWORD      = os.getenv('NEOS_PASSWORD')
NEOS_MACHINEID     = os.getenv('NEOS_MACHINEID')
EVAL_INTERVAL      = int(os.getenv('EVAL_INTERVAL'))

client = discord.Client(intents=discord.Intents.default())

token = ""
ownerID = ""

async def update():

    global token
    global ownerID

    async with aiohttp.ClientSession() as session:
        result_r = await session.get(f"https://api.neos.com/api/users/{ownerID}/friends",
                                      headers={
                                            'Content-Type': 'application/json',
                                            'Authorization': token
                                          })
        print(result_r, file=sys.stderr)
        result_j = await result_r.json()
        print(result_j, file=sys.stderr)

        newmsg = f'**ONLINE LIST** (edited: <t:{math.floor(time.time())}:R> )' + '\n'
        newmsg += MESSAGE_PREFIX + '\n'
        newmsg += '\n'.join(list(
            map(lambda x: f"{x['friendUsername']}: {x['userStatus']['onlineStatus']}@{x['userStatus'].get('currentSession', {}).get('name', 'Private')} ({x['userStatus']['outputDevice']})",
                filter(lambda x: x['userStatus']['onlineStatus'] != 'Offline', result_j))))

        channel = client.get_channel(DISCORD_CHANNEL_ID)
        message = await channel.fetch_message(DISCORD_MESSAGE_ID)
        await message.edit(content=newmsg)
        with open('/tmp/healthy', 'a') as fp:
            pass

@client.event
async def on_ready():

    global token
    global ownerID

    async with aiohttp.ClientSession() as session:
        result_r = await session.post("https://api.neos.com/api/userSessions",
                                      headers={'Content-Type': 'application/json'},
                                      json={"username": NEOS_USERNAME, "password": NEOS_PASSWORD, "secretMachineId": NEOS_MACHINEID})
        print(result_r, file=sys.stderr)
        result_j = await result_r.json()
        print(result_j, file=sys.stderr)
        ownerID = result_j['userId']
        token = f"neos {result_j['userId']}:{result_j['token']}"

    while True:
        await update()
        await asyncio.sleep(EVAL_INTERVAL)

client.run(DISCORD_BOT_TOKEN)

