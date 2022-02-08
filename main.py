from telethon import events
import heroku3
from mongo import HerokuApisDB

from config import bot, main_group_id

apidb = HerokuApisDB()

@bot.on(events.NewMessage(pattern=f"/start"))
async def _(event):
    if event.text == '/start' or event.text == '/start@Dio_Brando_Robot':
        await event.reply("You were expecting a welcome but,", file='https://c.tenor.com/WI1--JsW33EAAAAC/dio-jojo.gif')
        

@bot.on(events.NewMessage(pattern=f"/off", chats=main_group_id))
async def _(event):
    try:
        username = event.text.replace('/off', '')
        username = username.strip()
        print(username)
        data = apidb.find({'_id':username})
        print(data)
        heroku3.from_key(data['key'][1]).apps()[data['key'][0]].process_formation()['worker'].scale(0)
        await event.reply(f"{username} is now dead.")
    except Exception as e:
        await event.reply(str(e))

@bot.on(events.NewMessage(pattern=f"/on"), chats=main_group_id)
async def _(event):
    try:
        username = event.text.replace('/on', '')
        username = username.strip()
        data = apidb.find({'_id':username})
        heroku3.from_key(data['key'][1]).apps()[data['key'][0]].process_formation()['worker'].scale(1)
        await event.reply(f"{username} is now Alive.")
    except Exception as e:
        await event.reply(str(e))

@bot.on(events.NewMessage(pattern=f"/addapi"), chats=main_group_id)
async def _(event):
    try:
        _, username, appname, apikey = event.text.split(" ")
        apidb.add({'_id':username, 'key': [appname, apikey]})
        await event.reply(f"Added to DB:\nUsername: {username}\nAppname: {appname}\nKey: {apikey}")
    except Exception as e:
        await event.reply(e)

@bot.on(events.NewMessage(pattern=f"/removeapi"), chats=main_group_id)
async def _(event):
    try:
        _, username = event.text.split(" ")
        apidb.remove({'_id':username})
        await event.reply(f"Removed from DB:\nUsername: {username}")
    except Exception as e:
        await event.reply(e)

@bot.on(events.NewMessage(pattern=f"/allapi"), chats=main_group_id)
async def _(event):
    try:
        s = ''
        for i in apidb.full():
            s = s + i['_id'] + '\n'
        await event.reply(s)
    except Exception as e:
        await event.reply(e)
  


bot.start()

bot.run_until_disconnected()
