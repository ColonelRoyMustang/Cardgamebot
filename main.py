import discord
import random
from PIL import Image
import os
def combine(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

class MyClient(discord.Client):
    async def on_ready(self):
        print("Eingeloggt")
        self.pokerlist_original = ["Herz_2", "Herz_3", "Herz_4", "Herz_5", "Herz_6", "Herz_7", "Herz_8", "Herz_9",
                                   "Herz_10", "Herz_Bube", "Herz_Dame", "Herz_Koenig", "Herz_Ass", "Karo_2", "Karo_3",
                                   "Karo_4", "Karo_5", "Karo_6", "Karo_7", "Karo_8", "Karo_9", "Karo_10", "Karo_Bube",
                                   "Karo_Dame", "Karo_Koenig", "Karo_Ass", "Kreuz_2", "Kreuz_3", "Kreuz_4", "Kreuz_5",
                                   "Kreuz_6", "Kreuz_7", "Kreuz_8", "Kreuz_9", "Kreuz_10", "Kreuz_Bube", "Kreuz_Dame",
                                   "Kreuz_Koenig", "Kreuz_Ass", "Pieck_2", "Pieck_3", "Pieck_4", "Pieck_5", "Pieck_6",
                                   "Pieck_7", "Pieck_8", "Pieck_9", "Pieck_10", "Pieck_Bube", "Pieck_Dame",
                                   "Pieck_Koenig", "Pieck_Ass"]
        self.pokerlist = self.pokerlist_original.copy()
        self.counter = 0
        self.playerlist = {}
        self.moneylist = {}
        self.actioncounter ={}
        self.text = None
        self.pot = 0
        self.highest = 0
        f = open("Server_id.txt", "r")
        self.id = int(f.read())
        if self.id != "":
            channel = client.get_channel(self.id)
            f.close()
            em = discord.Embed(color=discord.Colour.orange())
            em.title = "Let us play cards!"
            em.description = "p-... --> Poker \n?-... --> Coming soon!"
            text = await channel.send(embed=em)
        else:
            f.close()
            self.id = None
            pass
    async def on_message(self, message):

        if message.content == "p-setchannel":
            f = open("Server_id.txt", "w")
            f.write(f"{message.channel.id}")
            f.close()
            self.id = message.channel.id
            await message.add_reaction("✅")

        elif message.content == "p-handout":
            #await message.delete()
            
            self.counter += 1
            if self.counter == 1:
                for i in range(3):
                    if i == 0:
                        x = random.randint(0, len(self.pokerlist)-1)
                        Image.open(f"Poker/Einzelnde Karten/{self.pokerlist[x]}.png").save("board.png")
                        self.pokerlist.pop(x)
                    else:
                        x = random.randint(0, len(self.pokerlist) - 1)
                        combine(Image.open("board.png"),
                                Image.open(f"Poker/Einzelnde Karten/{self.pokerlist[x]}.png")).save(
                            "board.png")
                        self.pokerlist.pop(x)
                file = discord.File("board.png")
                em = discord.Embed(color=discord.Colour.orange(), title="Card laid!")
                em.set_image(url=f"attachment://board.png")
                channel = client.get_channel(self.id)
                self.text = await channel.send(file=file, embed=em)
            else:
                x = random.randint(0, len(self.pokerlist) - 1)
                combine(Image.open("board.png"),
                        Image.open(f"Poker/Einzelnde Karten/{self.pokerlist[x]}.png")).save(
                    "board.png")
                em = discord.Embed(color=discord.Colour.orange(), title="Card laid!")
                em.set_image(url=f"attachment://board.png")
                file = discord.File("board.png")
                await self.text.delete()
                channel = client.get_channel(self.id)
                self.text = await channel.send(file=file, embed=em)
                self.pokerlist.pop(x)

        elif message.content == "p-shuffle":
            try:
                os.remove("board.png")
            except:
                pass
            self.counter = 0
            self.pokerlist = self.pokerlist_original.copy()
            self.pot = 0
            for i in self.playerlist.keys():
                self.playerlist[i] = []
            random.shuffle(self.pokerlist)
            print(self.pokerlist)

        elif message.content == "p-add":
            self.playerlist[f"{message.author.id}"] = []
            self.moneylist[f"{message.author.id}"] = 0
            self.actioncounter[f"{message.author.id}"] = [0, 0]
            print(self.playerlist)
            print(self.moneylist)
            print(self.actioncounter)
            await message.add_reaction("✅")

        elif message.content == "p-giveout":

            if len(self.playerlist.keys()) == 0:
                await message.channel.send("There are no players yet!")
            else:
                for i in self.playerlist.keys():
                    for j in range(2):
                        if j == 0:
                            r = random.randint(0, len(self.pokerlist) - 1)
                            self.playerlist[i].append(self.pokerlist[r])
                            Image.open(f"Poker/Einzelnde Karten/{self.pokerlist[r]}.png").save(f"Players/Player{i}.png")
                            self.pokerlist.pop(r)
                        else:
                            r = random.randint(0, len(self.pokerlist) - 1)
                            self.playerlist[i].append(self.pokerlist[r])
                            combine(Image.open(f"Players/Player{i}.png"), Image.open(f"Poker/Einzelnde Karten/{self.pokerlist[r]}.png")).save(f"Players/Player{i}.png")
                            self.pokerlist.pop(r)
                    user = await client.fetch_user(int(f"{i}"))
                    await user.send(file=discord.File(f"Players/Player{i}.png"))
                print(self.playerlist)

        elif message.content.startswith("p-setmoney"):
            if message.author == client.user:
                return
            elif str(message.author.id) not in list(self.playerlist.keys()):
                await message.channel.send(content=f"{message.author.mention} you do not play with them!")
                await message.add_reaction("❌")
            else:

                temp = message.content.split(" ")

                if len(temp) != 2 or not temp[1].isdigit():
                    await message.channel.send(content="p-setmoney -amount of money as a natural number!-")
                    await message.add_reaction("❌")
                else:
                    self.moneylist[str(message.author.id)] += int(temp[1])
                    txt = await message.channel.send(f"{message.author.mention} you have now {self.moneylist[str(message.author.id)]} silver at your account!")



        elif message.content == "p-revealall":
            for i in self.playerlist.keys():
                user = await client.fetch_user(int(f"{i}"))
                combine(Image.open(f"Poker/Einzelnde Karten/{self.playerlist[i][0]}.png"), Image.open(f"Poker/Einzelnde Karten/{self.playerlist[i][1]}.png")).save(
                    "temp.png")
                file = discord.File("temp.png")
                em = discord.Embed(color=discord.Colour.orange(), title=f"Handcards of {user.name}")
                em.set_image(url=f"attachment://temp.png")
                channel = client.get_channel(self.id)
                text = await channel.send(file=file, embed=em)

        elif message.content.startswith("p-raise"):

            if message.author == client.user:
                return
            elif str(message.author.id) not in list(self.playerlist.keys()):
                await message.channel.send(content=f"{message.author.mention} you do not play with them!")
                await message.add_reaction("❌")
            elif self.actioncounter[str(message.author.id)][0] != 0:
                await message.channel.send(content=f"{message.author.mention} you are finished")
                await message.add_reaction("❌")

            else:

                temp = message.content.split(" ")

                if len(temp) != 2 or not temp[1].isdigit():
                    await message.channel.send(content="p-raise -amount of money as a natural number!-")
                    await message.add_reaction("❌")

                else:

                    if self.moneylist[str(message.author.id)] == 0 or self.moneylist[str(message.author.id)]-int(temp[1]) < 0:
                        await message.channel.send(content=f"{message.author.mention} you are broke or the raise is too much!")
                        await message.add_reaction("❌")
                    elif int(temp[1]) <= self.highest:
                        txt = await message.channel.send(f"{message.author.mention} that is not a raise....")
                    else:

                        self.moneylist[str(message.author.id)] -= int(temp[1])
                        self.pot += int(temp[1])
                        self.highest = int(temp[1])
                        self.actioncounter[str(message.author.id)][0] = 1
                        self.actioncounter[str(message.author.id)][1] = self.highest
                        txt = await message.channel.send(f"{message.author} is raising!\nCurrent highest bet: {self.highest} silver!\nThe Pot now contains {self.pot} silver!")

        elif message.content == ("p-check"):

            if message.author == client.user:
                return
            elif str(message.author.id) not in list(self.playerlist.keys()):
                await message.channel.send(content=f"{message.author.mention} you do not play with them!")
                await message.add_reaction("❌")
            elif self.actioncounter[str(message.author.id)][0] != 0:
                await message.channel.send(content=f"{message.author.mention} you are finished")
                await message.add_reaction("❌")
            else:
                if self.moneylist[str(message.author.id)] == 0 or self.moneylist[str(message.author.id)] - self.highest < 0:
                    await message.channel.send(content="You are broke or the highest bet is too much for you!")
                    await message.add_reaction("❌")
                else:

                    self.moneylist[str(message.author.id)] -= self.highest - self.actioncounter[str(message.author.id)][1]
                    self.pot += self.highest - self.actioncounter[str(message.author.id)][1]
                    self.actioncounter[str(message.author.id)][0] = 1
                    self.actioncounter[str(message.author.id)][1] = self.highest
                    txt = await message.channel.send(
                        f"current highest bet: {self.highest} silver!\nThe Pot now contains {self.pot} silver!")

        elif message.content == ("p-throw"):
            if message.author == client.user:
                return
            elif str(message.author.id) not in list(self.playerlist.keys()):
                await message.channel.send(content=f"{message.author.mention} you do not play with them!")
                await message.add_reaction("❌")
            else:
                self.actioncounter[str(message.author.id)][0] = 3

        elif message.content == ("p-endround"):
            unfinished = []
            more = []
            alright = True
            textu = ""
            textm = ""
            for i in self.actioncounter.keys():
                if self.actioncounter[i] == 0:
                    unfinished.append(i)
                    alright = False
                elif self.actioncounter[i][0] == 1:
                    if self.actioncounter[i][1] < self.highest:
                        more.append([i,self.highest-self.actioncounter[i][1]])
                        alright = False
            if not alright:
                if len(unfinished) != 0:
                    for i in unfinished:
                        user = await client.fetch_user(int(f"{i[0]}"))
                        textu = textu + f"{user}\n"
                if len(more) != 0:
                    for i in more:
                        user = await client.fetch_user(int(f"{i[0]}"))
                        textm = textm + f"{user} {i[1]}\n"
                        self.actioncounter[str(message.author.id)][0] = 0
                if textm == "":
                    textm = "Nobody"
                if textu == "":
                    textu = "Nobody"
                em = discord.Embed(color=discord.Colour.orange(), title="Status")
                em.add_field(name="These are not done!", value=textu)
                em.add_field(name=f"Name -unpaid value-", value=textm)
                txt = await message.channel.send(embed=em)
            else:
                for i in self.actioncounter.keys():
                    self.actioncounter[i][0] = 0
                    self.actioncounter[i][1] = 0
                self.highest = 0

                txt = await message.channel.send("Next Round!")

        elif message.content == ("p-mymoney"):
            if message.author == client.user:
                return
            elif str(message.author.id) not in list(self.playerlist.keys()):
                await message.channel.send(content=f"{message.author.mention} you do not play with them!")
                await message.add_reaction("❌")
            else:
                txt = await message.channel.send(f"{message.author.mention} you currently have {self.moneylist[str(message.author.id)]} silver!")

        elif message.content == ("p-winner"):
            if message.author == client.user:
                return
            elif str(message.author.id) not in list(self.playerlist.keys()):
                await message.channel.send(content=f"{message.author.mention} you do not play with them!")
                await message.add_reaction("❌")
            else:
                self.moneylist[str(message.author.id)] += self.pot
                txt = await message.channel.send(f"{message.author.mention} Good job, you just won {self.pot} silver!")
                self.pot = 0
                for i in self.actioncounter.keys():
                    self.actioncounter[i][0] = 0
                    self.actioncounter[i][1] = 0
                self.highest = 0




client = MyClient()
client.run("ODg1MjMwOTQ0MzUxNTgwMTcw.YTkBjw.pC4KpbaNK135xNbXT8JPdTTEDHI")


