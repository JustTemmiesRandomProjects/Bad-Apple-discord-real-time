import discord
from discord.ext.commands import Bot
from discord.ext import commands

import asyncio
import time
from PIL import Image

import sys
import os

Total_Frames = 6515

OWNER_IDS = [368423564229083137]

ASCII_CHARS = ['⠀','⠄','⠆','⠖','⠶','⡶','⣩','⣪','⣫','⣾','⣿']
ASCII_CHARS.reverse()
ASCII_CHARS = ASCII_CHARS[::-1]

WIDTH = 60

TIMEOUT = 1/((int(Total_Frames)+1)/220)*18

def resize(image, new_width=WIDTH):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int((aspect_ratio * new_width)/2)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image

def greyscale(image):
    return image.convert('L')

def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

def do(image, new_width=WIDTH):
    image = resize(image)
    image = greyscale(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    new_image = [pixels[index:index+int(new_width)] for index in range(0, len_pixels, int(new_width))]

    return '\n'.join(new_image)

def runner(path):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        return
    image = do(image)

    return image

frames = []

for i in range(1, 232):
    path = "frames/frameframe/frame"+str(i*30+12)+".png"
    frames.append(runner(path))

bot = commands.Bot(
    command_prefix = "--",
    owner_ids=OWNER_IDS)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity = discord.Activity(type=discord.ActivityType.listening, name="!help"))
    print("Bot is connected to all of the available servers in the bots mainframe.")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@bot.event
async def on_message(message):

    if message.content.startswith('--apple'):
        
        i = 0
        
        time.sleep(0.4333333333)
        
        while i <= 695:
            await message.channel.send(frames[int(i)])
            time.sleep(1)
            i=i+1

    elif "bad apple" in message.content:
        await message.channel.send("did someone just mention bad apppplee??")

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@commands.is_owner()
@bot.command(name= "restart", aliases=["reboot"])
async def restart(ctx):
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="restarting - won\'t respond"))
    await ctx.send("Restarting bot...")
    restart_bot()

@commands.is_owner()
@bot.command(name= "shutdown", aliases=["poweroff", "turnoff"])
async def shutdown(ctx):
    await ctx.send("turning off the bot...")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="turning offline - won\'t respond"))
    await bot.close()
    print("closed using !shutdown command")

bot.run('TOKEN')