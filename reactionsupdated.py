import discord
from youtubesearchpython import VideosSearch
from youtube_dl import YoutubeDL
from keepalive import keep_alive
import os

TOKEN = "YOUR BOT TOKEN HERE"
cmd_prefix = "<"
reactions_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

helpwithbot = """
TUBOT - Best quality Audio downloader bot for Youtube
Easily download the audio of youtube videos you want to listen.
Search for any youtube video and choose the link to download it's audio.
Max Audio length to download - 20 Minutes
-------------------------
Commands
<h, <H, <help - Help

<ping - Check if the Bot works properly
return - "pong" string

<hello, <hi             
returns a greet message

<tubot {URL}
Download the audio from given url of youtube

<ytsearch               
arg - {search_term}
Searches youtube with the search term

<link {link_no}        
Run after searching  ytsearch cmd
link_no - Sno of the link you want to download from the video search
-------------------------
"""

def cmd_check(message):
    if str(message.content).startswith(cmd_prefix):
        return True
    return False

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")

def video_validity(url):
    audio_downloader = YoutubeDL({'format':'bestaudio'})
    info = audio_downloader.extract_info(url, download=False)
    # print(type(info['duration']))
    # print(info['duration'])
    if info['duration'] <= 20*60 and info['duration'] > 0:
        return True
    else:
        return False


class MyClient(discord.Client):
    response_req = 0
    videos = []
    url = ""

    async def on_ready(self):
        # don't respond to ourselves
        print('Logged on as', self.user)

    async def on_message(self, message):
        if cmd_check(message):
            if message.author == self.user:
                return

            if message.content[1:] == 'h' or message.content[1:] == 'help' or message.content[1:] == 'H':
                await message.channel.send(helpwithbot)
            
            if message.content[1:] == 'ping':
                await message.channel.send('pong')
                # print(message.channel)

            if message.content[1:].startswith("Hello"):
                await message.channel.send('Hello ' + str(message.author))
                print("hellomsg")

            if message.content[1:].startswith('ytsearch'):
                self.videos = []
                self.response_req = 1
                msg_recv = message.content[len('<ytsearch'):]
                
                searchterm = msg_recv
                videosSearch = VideosSearch(searchterm, limit = 10)

                result = "This is what I found\n\n"
                count = 0
                for i in videosSearch.result()["result"]:
                    count += 1
                    if i["duration"] and i["channel"]["name"]:
                        if count <= 3:
                            result += (reactions_numbers[count-1] + " " + i["title"] + "\n" + i["link"] + "\n" + i["duration"] + "  " + i["channel"]["name"] + "\n")
                        else:
                            result += (reactions_numbers[count-1] + " " + i["title"] + "\n" + i["duration"] + "  " + i["channel"]["name"] + "\n")
                    else:
                        result += (reactions_numbers[count-1] + " " + i["title"] + "\n")

                    self.videos.append(i["link"]) 
                await message.channel.send(result)
                await message.channel.send("Run <link> command to download the required video.....")


            if message.content[1:].startswith('link') and self.response_req == 1:
                #global videos
                self.response_req = 0
                msg_recv = int(message.content[len('<link'):])
                # url of the video
                url = self.videos[msg_recv - 1]
                if video_validity(url):
                    audio_downloader = YoutubeDL({'format':'bestaudio'})
                    info = audio_downloader.extract_info(url)
                    filename = audio_downloader.prepare_filename(info)

                    print("Downloaded")
                    await message.channel.send(file=discord.File(filename))
                    delete_file(filename)
                else:
                    await message.channel.send("Video too long or Invalid URL")

            if message.content[1:].startswith('tubot'):
                self.url = message.content[len('<tubot '):]
                if video_validity(self.url):
                # url of the video
                # url = self.videos[msg_recv]
                    await message.channel.send("Start Download?")
                else:
                    await message.channel.send("Video too long or Invalid URL")
                # audio_downloader = YoutubeDL({'format':'bestaudio'})
                # try:
                #     info = audio_downloader.extract_info(url)
                #     filename = audio_downloader.prepare_filename(info)
                #     print("Downloaded")
                #     await message.channel.send(file=discord.File(filename))
                # except:
                #     await message.channel.send("Invalid URL try again")

        elif message.author == self.user and message.content.startswith("This is what I found"):
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            await message.add_reaction("6️⃣")
            await message.add_reaction("7️⃣")
            await message.add_reaction("8️⃣")
            await message.add_reaction("9️⃣")
            await message.add_reaction("🔟")
        
        elif message.author == self.user and message.content.startswith("Start Download?"):
            await message.add_reaction("✅")
            await message.add_reaction("❎")



    async def on_reaction_add(self, reaction, user):
        if user != client.user and reaction.message.author == self.user:
            print("reaction det" + str(reaction.emoji))
            # if str(reaction.emoji) == "1️⃣":
            #     ind = 1
            # elif str(reaction.emoji) == "2️⃣":
            #     ind = 2
            # elif str(reaction.emoji) == "3️⃣":
            #     ind = 3
            # elif str(reaction.emoji) == "4️⃣":
            #     ind = 4
            # elif str(reaction.emoji) == "5️⃣":
            #     ind = 5
            # elif str(reaction.emoji) == "6️⃣":
            #     ind = 6
            # elif str(reaction.emoji) == "7️⃣":
            #     ind = 7
            # elif str(reaction.emoji) == "8️⃣":
            #     ind = 8
            # elif str(reaction.emoji) == "9️⃣":
            #     ind = 9
            # elif str(reaction.emoji) == "🔟":
            #     ind = 10
            if str(reaction.emoji) in reactions_numbers:
                ind = reactions_numbers.index(str(reaction.emoji)) + 1
            else:
                ind = 0
            # print(self.videos[ind-1])
            if ind != 0:
                url = self.videos[ind-1]
                if video_validity(url):
                    audio_downloader = YoutubeDL({'format':'bestaudio'})
                    await reaction.message.channel.send("PREPARING AUDIO FILE.........")
                    info = audio_downloader.extract_info(url)
                    filename = audio_downloader.prepare_filename(info)

                    print("Downloaded")
                    await reaction.message.channel.send(file=discord.File(filename))
                    delete_file(filename)
                else:
                    await reaction.message.channel.send("Video too long or Invalid URL")
            
            if reaction.message.content.startswith("Start Download?"):
                if str(reaction.emoji) == "✅":
                    audio_downloader = YoutubeDL({'format':'bestaudio'})
                    await reaction.message.channel.send("PREPARING AUDIO FILE.........")
                    try:
                        info = audio_downloader.extract_info(self.url)
                        filename = audio_downloader.prepare_filename(info)
                        print("Downloaded")
                        await reaction.message.channel.send(file=discord.File(filename))
                        delete_file(filename)
                        self.url = ""
                    except:
                        await reaction.message.channel.send("Invalid URL try again")
                        self.url = ""

                elif str(reaction.emoji) == "❎":
                    await reaction.message.channel.send("Download Cancelled")
                    self.url = ""




keep_alive()
client = MyClient()
client.run(TOKEN)