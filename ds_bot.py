import discord, sqlite3
from discord.ext import commands
from config import settings_ds
import database

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix = settings_ds['prefix'], intents=intent)


@bot.command() 
async def yo(ctx): 
    author = ctx.message.author 
    await ctx.send(f'Hello, {author.mention}!')

    
@bot.event
async def on_raw_reaction_add(payload):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    
    member = payload.member
    cur.execute("SELECT * FROM User WHERE discord='{discord}'".\
                format(discord=member))
    
    records = cur.fetchall()
    if not records:
        lololo = 123
    else:
        cur.execute("SELECT * FROM react WHERE id = 1")    
        records = cur.fetchall()   
        react_id = records[0][1]
        
        ourMessageID = react_id 
    
        if ourMessageID == payload.message_id:
            member = payload.member # определяем юзера
            guild = member.guild # определяем сервер
    
            emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
            if emoji == '✅': # само эмоджи
                role = discord.utils.get(guild.roles, id = 1009496968504025089) # определяем роль которую будем выдавать
                await member.add_roles(role) # выдаем рольку
    
    cur.execute("SELECT * FROM User WHERE discord='{discord}'".\
                format(discord=member))
    
    records = cur.fetchall()
    
    if not records:
        lololo = 123
    else:
        cur.execute("SELECT * FROM react WHERE id = 2")    
        records = cur.fetchall()   
        react_id = records[0][1]
        
        ourMessageID = react_id
    
        if ourMessageID == payload.message_id:
            member = payload.member # определяем юзера
            guild = member.guild # определяем сервер
    
            emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
            if emoji == '✅': # само эмоджи
                role = discord.utils.get(guild.roles, id = 1105657665532723210) # определяем роль которую будем выдавать
                await member.add_roles(role) # выдаем рольку


@bot.event
async def on_raw_reaction_remove(payload):
    con = sqlite3.connect("users.db")
    cur = con.cursor()     
    cur.execute("SELECT * FROM react WHERE id = 1")    
    records = cur.fetchall()   
    react_id = records[0][1]
    
    ourMessageID = react_id 

    if ourMessageID == payload.message_id:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
        if emoji == '✅': # само эмоджи
            role = discord.utils.get(guild.roles, id = 1009496968504025089) # определяем роль которую будем выдавать

            member = await(guild.fetch_member(payload.user_id))
            if member is not None: # проверяем есть ли он на сервере
                await member.remove_roles(role) # забираем рольку
            else:
                print('not found')
                  

@bot.command()
async def react(ctx):
    embed = discord.Embed(color = 0xff9900, title = 'Нажми реакцию, если готов!') # Создание Embed'a
    message = await ctx.send(embed = embed) # Отправляем Embed
    await message.add_reaction('✅')
    react = message.id
    con = sqlite3.connect("users.db")
    cur = con.cursor()     
    database.react_id(cur, con, react)


@bot.command()
async def check(ctx):
    embed = discord.Embed(color = 0xff9900, title = 'Нажми реакцию, для подтверждения аккаунта!') # Создание Embed'a
    message = await ctx.send(embed = embed) # Отправляем Embed
    await message.add_reaction('✅')
    react = message.id
    con = sqlite3.connect("users.db")
    cur = con.cursor()     
    database.check_id(cur, con, react)


#@bot.event
#async def on_raw_reaction_add_check(payload):
    #con = sqlite3.connect("users.db")
    #cur = con.cursor()
    
    #member = payload.member
    #cur.execute("SELECT * FROM User WHERE discord='{discord}'".\
                #format(discord=member))
    
    #records = cur.fetchall()
    
    #if not records:
        #lololo = 123
    #else:
        #cur.execute("SELECT * FROM react WHERE id = 2")    
        #records = cur.fetchall()   
        #react_id = records[0][1]
        
        #ourMessageID = react_id # айди сообщения (сначала создаем его командой !react, а потом копируем его айди и вписываем сюда)
    
        #if ourMessageID == payload.message_id:
            #member = payload.member # определяем юзера
            #guild = member.guild # определяем сервер
    
            #emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
            #if emoji == '✅': # само эмоджи
                #role = discord.utils.get(guild.roles, id = 1105657665532723210) # определяем роль которую будем выдавать
                #await member.add_roles(role) # выдаем рольку


#@bot.event
#async def on_raw_reaction_remove_check(payload):
    #con = sqlite3.connect("users.db")
    #cur = con.cursor()     
    #cur.execute("SELECT * FROM react WHERE id = 2")    
    #records = cur.fetchall()   
    #react_id = records[0][1]
    
    #ourMessageID = react_id # айди сообщения (сначала создаем его командой !react, а потом копируем его айди и вписываем сюда)

    #if ourMessageID == payload.message_id:
        #guild = await(bot.fetch_guild(payload.guild_id))
        #emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
        #if emoji == '✅': # само эмоджи
            #role = discord.utils.get(guild.roles, id = 1105657665532723210) # определяем роль которую будем выдавать

            #member = await(guild.fetch_member(payload.user_id))
            #if member is not None: # проверяем есть ли он на сервере
                #await member.remove_roles(role) # забираем рольку
            #else:
                #print('not found')


bot.run(settings_ds['token'])