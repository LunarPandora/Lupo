import os
import discord
import validators
import json
import requests
import random
import time
import tldextract
from dotenv import load_dotenv
from .utils import filter_word_number


load_dotenv()

lupo = discord.Client()

filter_mode = True
attitude_mode = False
owner_away = False
owner_work = False
lk_list = json.loads(requests.get('https://spen.tk/api/v1/links').text)["links"]
# lk_list = json.loads(requests.get('https://api.hyperphish.com/gimme-domains').text)

@lupo.event
# class Lupo(discord.Client):
async def on_ready():
    await lupo.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="how to code."))
    print("The bot is ready.")

@lupo.event    
async def on_message(msg):
    prefix = ">"
    
    if msg.author == lupo.user:
        return
    
    if msg.content[0] == prefix:
        cmd = msg.content[1:].split(" ")
        if ">" not in cmd[0]:
            if cmd[0] == "filter":
                if cmd[1] == "on":
                    globals()["filter_mode"] = True
                    await msg.channel.send("Link-filter mode have been turned on, <@" + str(msg.author.id) + ">.")
                        
                elif cmd[1] == "off":
                    globals()["filter_mode"] = False
                    await msg.channel.send("Link-filter mode have been turned off, <@" + str(msg.author.id) + ">.")
                else:
                    # print(msg.author.id)
                    await msg.channel.send("Sorry <@" + str(msg.author.id) + ">, i don't understand what you said.")
                    
            elif cmd[0] == "bl":
                try:
                    f = open('blacklist.json','r+')
                    data = json.load(f)
                    
                    for x in range(len(cmd)):
                        if x != 0:
                            if cmd[x] not in data["blacklisted"]:
                                data["blacklisted"].append(cmd[x])
                        
                    f.truncate(0)
                    f.seek(0)
                    json.dump(data, f)
                    f.close()
                                        
                except:                    
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                
                finally:
                    await msg.channel.send("The keyword(s) have been added to blacklist.")
                
            elif cmd[0] == "rmbl":
                try:
                    f = open('blacklist.json','r+')
                    data = json.load(f)
                    res = []
                    
                    for x in data["blacklisted"]:
                        if x not in res and x != cmd[1]:
                            res.append(x)
                            
                    data["blacklisted"] = res
                            
                    f.truncate(0)
                    f.seek(0)
                    json.dump(data, f)
                    f.close()
                
                except:                    
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                
                finally:
                    await msg.channel.send("The '" + cmd[1] + "' keyword have been removed from blacklist.")
                
            elif cmd[0] == "keylist":
                try:
                    f = open('blacklist.json')
                    data = json.load(f)
                    words = ", ".join(data["blacklisted"])
                    f.close()
                    
                    embed = discord.Embed(
                        title="Banned link keyword list",
                        description=words,
                        color=0x0197CA
                    )
                    
                except:                    
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                
                finally:
                    await msg.channel.send(embed=embed)
            
            elif cmd[0] == "sw":
                try:
                    f = open('swearjar.json','r+')
                    data = json.load(f)
                    
                    for x in range(len(cmd)):
                        if x != 0:
                            if cmd[x] not in data["badwords"]:
                                data["badwords"].append(filter_word_number(cmd[x]))
                        
                    f.truncate(0)
                    f.seek(0)
                    json.dump(data, f)
                    f.close()
                                        
                except:                    
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                
                finally:
                    await msg.channel.send("The swearword(s) have been added to blacklist.")
                    
            elif cmd[0] == "rmsw":
                try:
                    f = open('swearjar.json','r+')
                    data = json.load(f)
                    res = []
                    
                    for x in data["badwords"]:
                        if x not in res and x != cmd[1]:
                            res.append(filter_word_number(x))
                            
                    data["badwords"] = res
                            
                    f.truncate(0)
                    f.seek(0)
                    json.dump(data, f)
                    f.close()
                
                except:                    
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                
                finally:
                    await msg.channel.send("The '" + cmd[1] + "' keyword have been removed from blacklist.")
                
            elif cmd[0] == "attitude":
                if cmd[1] == "on":
                    globals()["attitude_mode"] = True
                    await msg.channel.send("Swear-word-filter mode have been turned on, <@" + str(msg.author.id) + ">. Better behave, kids.")
                    
                elif cmd[1] == "off":
                    globals()["attitude_mode"] = False
                    await msg.channel.send("Swear-word-filter mode have been turned off, <@" + str(msg.author.id) + ">. Finally, some rest.")
                    
                else:
                    # print(msg.author.id)
                    await msg.channel.send("Sorry <@" + str(msg.author.id) + ">, i don't understand what you said.")
            
            elif cmd[0] == "catch":
                if msg.guild.id == int(os.getenv('ROOT_GUILD')):
                    try:
                        member = await msg.guild.query_members(user_ids=int(cmd[1][2:-1]))
                        await member[0].add_roles(msg.guild.get_role(int(os.getenv('ROLE_QUARANTINE'))))
                        
                    except:
                        await msg.channel.send("Failed to quarantine " + cmd[1] + "!")
                        
                    finally:
                        await msg.channel.send(cmd[1] + " have been quarantined.")
                else:
                    await msg.channel.send("This command is only available on main server. Please contact my master for more information.")
                    
            elif cmd[0] == "sleep":
                if msg.guild.id == int(os.getenv('ROOT_GUILD')):
                    try:
                        member = await msg.guild.query_members(user_ids=int(cmd[1][2:-1]))
                        await member[0].add_roles(msg.guild.get_role(int(os.getenv('ROLE_INACTIVATED'))))
                        
                    except:
                        await msg.channel.send("Failed to inactivating " + cmd[1] + "!")
                        
                    finally:
                        await msg.channel.send(cmd[1] + " have been inactivated.")
                else:    
                    await msg.channel.send("This command is only available on main server. Please contact my master for more information.")
                    
            elif cmd[0] == "oafk":
                if msg.author.id == int(os.getenv('OWNER_ID')):
                    if cmd[1] == "on":
                        globals()["owner_away"] = True
                        globals()["owner_work"] = False
                        await msg.channel.send("Okay master, have a good rest.")
                    
                    elif cmd[1] == "off":
                        globals()["owner_away"] = False
                        await msg.channel.send("Welcome back, master.")
                else:
                    await msg.channel.send("This command is only available for my master.")
                    
            elif cmd[0] == "owork":
                if msg.author.id == int(os.getenv('OWNER_ID')):            
                    if cmd[1] == "on":
                        globals()["owner_work"] = True
                        globals()["owner_away"] = False
                        await msg.channel.send("Okay master, have a good day.")
                    
                    elif cmd[1] == "off":
                        globals()["owner_work"] = False
                        await msg.channel.send("Welcome back, master.")
                else:
                    await msg.channel.send("This command is only available for my master.")
            
            elif cmd[0] == "rules":
                if msg.guild.id == int(os.getenv('ROOT_GUILD')):
                    try:
                        words = """
Sebelum join ke server ini, silahkan dibaca dulu peraturan nya ya demi kebaikan bersama kawan-kawan :benny:

1. Dilarang memulai drama / membuat post yang dapat memicu permasalahan diantara member-member didalam server.
2. Dilarang membahas topik-topik yang bersifat / mengarah ke politik atau propaganda.
3. Dilarang meng-spam para Moderator secara terus menerus. Jika hal ini terjadi, maka kamu akan di kick/di ban dari server ini.
4. Dilarang mengirimkan konten-konten bersifat pornografi, kekerasan, atau SARA di channel-channel yang berlaku secara umum. Jika hal ini terjadi, maka kamu akan di ban dari server ini.
5. Gunakan channel yang tersedia dengan baik dan sesuai kegunaannya.
6. Mengikuti pedoman aturan-aturan yang telah ditentukan oleh Discord.
7. Untuk pembagian link-link berupa game "crack" atau link yang tidak dikenal, harap kirimkan ke <#939201527384518707> dan minta @Game Finder untuk mengecek keaslian dan keamanan link tersebut. Link yang tidak diverifikasi atau berpotensi merusak / berbahaya akan dihapus oleh Moderator dan @Game Finder.

Kalian dapat me-mention para admin dan owner yang memiliki role @Leader @Manager @Co-Manager @Trainee Moderator 

Peraturan Promosi (Khusus untuk @Merchants)

1. DIlarang mempromosikan hal-hal yang berbahaya seperti alat-alat senjata api, obat-obatan berbahaya, pergerakan-pergerakan separatis / hal-hal berbau SARA, dan hal-hal berbau pornografi / kekerasan.
2. Jika ingin mempromosikan sesuatu dalam server ini, harap mempromosikan nya di <#887707535627403295>, dan harap menghubungi Admin / Moderator server ini terlebih dahulu untuk role @Merchants)
                        """
                        
                        embed = discord.Embed(
                            title="Rules on Chill Cafe",
                            description=words,
                            color=0x0197CA
                        )
                        
                    except:                    
                        await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                    
                    finally:
                        await msg.channel.send(embed=embed)
                else:    
                    await msg.channel.send("This command is only available on main server. Please contact my master for more information.")
                    
            elif cmd[0] == "dice":
                try:
                    await msg.channel.send("Your dice landed on **" + str(random.randint(1, 6)) + "**!")
                    
                except:                    
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                    
            elif cmd[0] == "fslip":
                try:
                    res = random.randint(1, 6)
                    if(res == 1):
                        await msg.channel.send("Your fortune slip result for today is **Great Fortune**!")
                    elif(res == 2):
                        await msg.channel.send("Your fortune slip result for today is **Good Fortune**!")
                    elif(res == 3):
                        await msg.channel.send("Your fortune slip result for today is **Modest Fortune**!")
                    elif(res == 4):
                        await msg.channel.send("Your fortune slip result for today is **Rising Fortune**!")
                    elif(res == 5):
                        await msg.channel.send("Your fortune slip result for today is **Misfortune**!")
                    elif(res == 6):
                        await msg.channel.send("Your fortune slip result for today is **Great Misfortune**!")
                    
                except:                    
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                    
            elif cmd[0] == "refresh":
                try:
                    globals()["lk_list"] = json.loads(requests.get('https://spen.tk/api/v1/links').text)["links"]
                    
                except:
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                    
                finally:
                    await msg.channel.send("Library refreshed!")    
                    
            elif cmd[0] == "generate":
                if msg.author.id == int(os.getenv("OWNER_ID")):
                    try:                      
                        for x in range(0, 10):
                            rng = random.randint(0, len(globals()["lk_list"]) - 1)
                            await msg.channel.send("https://" + globals()["lk_list"][rng])
                                                        
                    except:
                        await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                        
                    finally:
                        await msg.channel.send("Generated links.")
                    
            elif cmd[0] == "clean":
                try:
                    c = 0
                    reply = await msg.channel.send("Please wait while i check and clean this channel...")
                    
                    msg_list = await msg.channel.history().flatten()
                    f = open('blacklist.json','r+')
                    data = json.load(f)
                    
                    for x in range(0, len(msg_list) - 1):
                        text = msg_list[x].content.replace("\n", " ").replace("(", "").replace(")", "").split(" ")
                        
                        for y in text:
                            
                            if(not validators.url(y)):
                                y = "https://" + y
                                
                            url = tldextract.extract(y)
                            
                            if url.subdomain != "":
                                url = url.subdomain + "." + url.domain + "." + url.suffix
                            else:
                                url = url.domain + "." + url.suffix
                            
                            if url in globals()["lk_list"]:
                                c += 1
                                await msg_list[x].delete()
                            else:
                                a = y.replace("https://", "").replace("http://", "").split("/")
                                b = ""
                                
                                if a[0] == "bit.ly":
                                    b = a[0] + "/" + a[1]
                                    
                                if a[0] in data["blacklisted"] or b in data["blacklisted"]:
                                    c += 1
                                    await msg_list[x].delete()
                                
                    await reply.delete()
                    f.close()
                                
                except:
                    await msg.channel.send("An error occured! Please kindly contact the Admin immediately to fix the issue.")
                    
                finally:
                    await msg.channel.send("Clean! Around " + str(c) + " suspicious link(s) already deleted! Please check again if there is any more suspicious links!")

            # elif cmd[0] == "pvc":
            #     guild = lupo.guild
            #     category = discord.utils.get(lupo.guild.categories, id=741545087229624391)
                
            #     rules = {
            #         guild.default_role: discord.PermissionOverwrite(connect = False, speak = False),    
            #         guild.query_members(user_ids=int(cmd[1][2:-1])): 
            #     }
                
            #     channel = await msg.guild.create_voice_channel(str(msg.author.display_name), category=category., overwrites=rules)
            
            else:
                await msg.channel.send("Sorry <@" + str(msg.author.id) + ">, i don't understand your command.")
    else:
        if filter_mode:
            f = open('blacklist.json')
    
            data = json.load(f)
            
            for x in msg.content.split(" "):
                if(validators.url(x)):
                    # if(x[-1] == "/"):
                    #     x = x[:-1]
                    
                    x = tldextract.extract(x)
                    if x.subdomain != "":
                        x = x.subdomain + "." + x.domain + "." + x.suffix
                    else:
                        x = x.domain + "." + x.suffix

                    if x in data["blacklisted"] or x in globals()["lk_list"]:
                        time.sleep(0.5)
                        target = await msg.channel.fetch_message(msg.id)
                        await target.delete()
                        time.sleep(1)
                        await msg.channel.send("The link is already deleted! If it was a wrong link, please kindly contact Admin to remove it from the blacklist.")
                        
            f.close()
            
        if attitude_mode:
            f = open('swearjar.json')
    
            data = json.load(f)
            
            for i in msg.content.lower().split(" "):
                i = filter_word_number(i)
                for j in range(len(data["badwords"])):
                    if data["badwords"][j] in i:
                        time.sleep(0.5)
                        target = await msg.channel.fetch_message(msg.id)
                        await target.delete()
                        time.sleep(1)
                        await msg.channel.send("Sheesh <@" + str(msg.author.id) + ">, that's rude. I have to delete that.")
                        
            f.close()
        
        if owner_away:
            if "<" + os.getenv("OWNER_ID") + ">" in msg.content:
                await msg.channel.send("My creator, <" + os.getenv("OWNER_ID") + "> is currently away. Try to contact him later.")
                
        if owner_work:
            if "<@695281927745437746>" in msg.content:
                await msg.channel.send("My creator, <@" + os.getenv("OWNER_ID") + "> is currently working at his office. Try to contact him later.")
                    
# client = Lupo()
# PORT = os.environ.get('PORT')
# lupo.loop.create_task(app.run_task('0.0.0.0', PORT))

lupo.run(os.getenv('BOT_TOKEN'))
