#!/usr/bin/env python36
# -*- coding: utf-8 -*-

from discord.ext import commands
from discord import Game, FFmpegPCMAudio
from secrets import get_token
import aiohttp, asyncio, json

if __name__ == "__main__":
	mode = "fenomen"

client = commands.Bot(command_prefix='!')
streams = {"fenomen": "https://listen.radyofenomen.com/fenomen/128/icecast.audio",
"fenomenturk": "https://listen.radyofenomen.com/fenomenturk/128/icecast.audio",
"fenomenyaz": "http://fenomenyaz.listenfenomen.com/fenomenyaz/128/icecast.audio",
"fenomenturkrap": "https://listen.radyofenomen.com/fenomenturkrap/128/icecast.audio",
"fenomenkpop": "https://listen.radyofenomen.com/fenomenkpop/128/icecast.audio",
"fenomenkarisik": "https://listen.radyofenomen.com/fenomenkarisik/128/icecast.audio",
"fenomenpop": "https://listen.radyofenomen.com/fenomenpop/128/icecast.audio",
"fenomendans": "https://listen.radyofenomen.com/fenomendans/128/icecast.audio",
"fenomenclubbin": "https://listen.radyofenomen.com/fenomenclubbin/128/icecast.audio",
"fenomenrap": "https://listen.radyofenomen.com/fenomenrap/128/icecast.audio",
"fenomenakustik": "https://listen.radyofenomen.com/fenomenakustik/128/icecast.audio",
"fenomenoriental": "https://listen.radyofenomen.com/fenomenoriental/128/icecast.audio"}


@client.command(name='mode', pass_context=True)
async def print_mode(ctx, arg=None):
	await ctx.send("Station mode: {0}".format(mode))


@client.command(name='np', pass_context=True)
async def now_playing(ctx, arg=None):
	session = aiohttp.ClientSession()
	response = await session.post("https://api.radyofenomen.com/Channels/?appRef=FenomenWebV2")
	data = json.loads(await response.text())
	await session.close()

	artist, song = "", ""
	global mode
	local_mode = mode
	if local_mode == "fenomen":
		local_mode = "radyofenomen"
	elif local_mode == "fenomenclubbin":
		local_mode = "clubbin"

	for obj in data.get("response"):
		print(obj.get("channel_seo_name"))
		if obj.get("channel_seo_name") == local_mode:
			info = obj.get("timeline")[0]
			artist = info.get("artistTitle")
			song = info.get("songTitle")
			break
	await ctx.send("Now Playing On {}: {} - {}".format(mode, artist, song))
	


@client.command(name='station', pass_context=True)
async def set_mode(ctx, arg=None):
	if not arg or arg not in streams.keys():
		stations = ", ".join(streams.keys())
		await ctx.send("Invalid station. Options: {}".format(stations))
		return

	global mode
	mode = arg
	await ctx.send("Station mode set to: {}".format(mode))
	if ctx.voice_client and ctx.voice_client.is_connected():
		ctx.voice_client.source = FFmpegPCMAudio(streams.get(mode))


@client.command(name='play', pass_context=True)
async def play(ctx):
	author = ctx.message.author
	channel = author.voice.channel if author.voice else None
	if not channel or not mode:
		await ctx.send("You have to be in a voice channel in order to use this command!")
		return
	
	await ctx.send("Playing {0}".format(mode))
	global voice_channel
	voice_channel = await channel.connect()
	voice_channel.play(FFmpegPCMAudio(streams.get(mode)), after=lambda e: print('Audiostream Ended With: ', e))


@client.command(name='leave', pass_context=True)
async def leave(ctx):
	if ctx.voice_client and ctx.voice_client.is_connected():
		await ctx.send("Left from {0}".format(ctx.voice_client.channel))
		await ctx.voice_client.disconnect()
		global voice_channel
		voice_channel = None
		return

	await ctx.send("Not connected to any channel.")


@client.event
async def on_ready():
	await client.change_presence(activity=Game(name="!help"))
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_disconnect():
	global voice_channel
	if voice_channel:
		voice_channel.disconnect()
		voice_channel = None


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	await client.process_commands(message)



client.run(get_token())