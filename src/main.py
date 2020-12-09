#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands, timers
import random
import json
import os
import asyncio
import datetime
from random import randint

# config stuff
token = str(os.environ['DISCORD_API_TOKEN'])
random_joins = str(os.environ['ENABLE_RANDOM_JOINS']).lower()
logging_channel = int(os.environ['LOGGING_CHANNEL'])
client = commands.Bot(command_prefix=commands.when_mentioned_or("!"),description='Buttergolem Discord Bot')
client.timer_manager = timers.TimerManager(client)


# simple log function
async def _log(message):
    channel = client.get_channel(logging_channel)
    await channel.send("```\n" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S # ") + str(message) + "```\n")


# Do this on ready (when joining)
@client.event
async def on_ready():
    if logging_channel: await _log("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")
    if logging_channel: await _log("⏳           joining server           ⏳")
    if logging_channel: await _log("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")

    if random_joins == "true":
        # start first timer for random geschrei
        if logging_channel: await _log("⏲ setting first timer...")
        await create_random_timer(1, 1)


# select the voicechannel with the most members in it (atm)
async def get_biggest_vc():
    if logging_channel: await _log("⤷ getting biggest vc...")

    # use the first (and hopefully only) guild of the client
    guild = client.guilds[0]

    if logging_channel: await _log("    ⤷ 🏰 " + guild.name)

    # initialize with the first voice channel on the guild
    voice_channel_with_most_users = guild.voice_channels[0]

    # go through every voice channel in the guild
    logtext = ""
    for voice_channel in guild.voice_channels:
        # find the one with the most users
        logtext += "\n    ⤷ " + str(len(voice_channel.members)) + " user in " + voice_channel.name
        if len(voice_channel.members) > len(voice_channel_with_most_users.members):
            voice_channel_with_most_users = voice_channel

    #if logging_channel: await _log("    ⤷ checking " + voice_channel.name + ", got " + str(len(voice_channel.members)) + " users")
    if logging_channel: await _log(logtext)
    if logging_channel: await _log("    ⤷ 🏁 found biggest vc: " + voice_channel_with_most_users.name)

    return voice_channel_with_most_users


# joins the voicechannel from ctx.message.author
# plays "soundfile.mp3" which should be /app/data/clips/soundfile.mp3
async def playsound(voice_channel, soundfile):
    # create StreamPlayer
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio('/app/data/clips/' + str(soundfile)), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    # disconnect after the player has finished
    await vc.disconnect()


# get a random datetime object between x (min) to y (max) minutes in the future
def get_random_datetime(min, max):
    randomdatetime = datetime.datetime.now() + datetime.timedelta(minutes=randint(min, max))
    return randomdatetime


# create timer
async def create_random_timer(min, max):
    # time has to be datetime.datetime object

    # get a random time in the next min-max minutes
    endtime = get_random_datetime(min, max)

    # start timer
    timers.Timer(client, "reminder", endtime).start()
    if logging_channel: await _log("⤷ timer set! ringing next: " + endtime.strftime("%d-%m-%Y %H:%M:%S"))


# get random filename from /app/data/clips
def get_random_clipname():
    all_clips = os.listdir('/app/data/clips')
    return str(random.choice(all_clips))


# this will run when the last timer rings
@client.event
async def on_reminder():
    if logging_channel: await _log("🟠 timer ringing! playing sound...")
    # play random sound in the most populated vc
    await playsound(await get_biggest_vc(), get_random_clipname())

    # create next timer
    if logging_channel: await _log("⤷ ⏲ setting new timer...")
    await create_random_timer(30, 60)


# Quotes stuff
@client.command(pass_context=True)
async def zitat(ctx):
    quotes_jsonfile = open('/app/data/quotes.json', mode="r", encoding="utf-8")
    buttergolem_quotes = json.load(quotes_jsonfile)
    names_jsonfile = open('/app/data/names.json', mode="r", encoding="utf-8")
    buttergolem_names = json.load(names_jsonfile)

    if ctx.message.author == client.user:
        return

    name = random.choice(buttergolem_names)
    quote = random.choice(buttergolem_quotes)
    response = str(name) + " sagt: " + str(quote)

    await ctx.message.channel.send(response)


# play random sound in channel of sender
@client.command(pass_context=True)
async def lord(ctx):
    # grab the user who sent the command
    user = ctx.message.author

    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, get_random_clipname())
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


# some ids for you
@client.command(pass_context=True)
async def id(ctx):
    # grab the user who sent the command
    user = ctx.message.author

    await ctx.message.channel.send('Current text_channel ID: ' + str(ctx.message.channel.id))
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await ctx.message.channel.send('Current voice_channel ID: ' + str(voice_channel.id))


# Commands for different sounds
@client.command(pass_context=True)
async def warum(ctx):
    # grab the user who sent the command
    user = ctx.message.author

    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "warum.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


@client.command(pass_context=True)
async def frosch(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "frosch.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


@client.command(pass_context=True)
async def furz(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "furz.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


@client.command(pass_context=True)
async def idiot(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "idiot.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


@client.command(pass_context=True)
async def meddl(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "meddl.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


@client.command(pass_context=True)
async def scheiße(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "scheiße.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


@client.command(pass_context=True)
async def durcheinander(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "Durcheinander.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


@client.command(pass_context=True)
async def wiebitte(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    if hasattr(ctx.message.author, "voice"):
        voice_channel = ctx.message.author.voice.channel
        await playsound(voice_channel, "Wiebitte.mp3")
    else:
        await ctx.message.channel.send('Das funktioniert nur in serverchannels du scheiß HAIDER')


client.run(token)
