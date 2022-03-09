from discord.ext import commands
import discord
from simpleNoten import SimpleNoten
import re

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix="\\")
noten1 = None

@client.event
async def on_ready(): 
    activity = discord.Activity(name="8.132 an der Tafel", type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print(f"ready")
    global noten1
    noten1 = SimpleNoten()


#@client.event
#async def on_command_error(ctx, error):
    #await ctx.send(f"```{error}```")


@client.command(brief="[Nachname der Person]", description="Zeigt die aktuellen Noten an (ohne Paramter --> deine Noten, "
                                                       "mit Paramter --> die Noten der jeweligen Person")
async def noten(ctx, person=None):
    print(f"noten")
    global noten1
    noten1 = SimpleNoten()
    embed = discord.Embed(title="** **", colour=discord.Colour.blue())
    print("before if")
    if person is None:
        notenPerson = noten1.getNoten(personId=ctx.author.id)
        userName = ctx.author.nick
        if userName is None:
            userName = ctx.author.display_name
        embed.set_author(name=userName,
                         icon_url=ctx.author.avatar_url,
                         url="https://www.htl-kaindorf.at/schule/schueler-innen#3BHIF")
    else:
        person = person.lower()
        personId = noten1.getID(person)
        print("PersonID " + personId)
        personId = int(personId)
        #print(type(personId))
        notenPerson = noten1.getNoten(personId)
        #print(notenPerson)
        user = await client.fetch_user(personId)
        guild = ctx.guild
        memberList = guild.members
        #print("MemberList")
        #print(memberList)
        #print(user)
        for x in memberList:
            if user.id == x.id:
               user = x
               break
        if user is not None:
            userName = user.display_name
            userAvatarUrl = user.avatar_url
            if userName is None:
               userName = user.display_name
        else:
            userName = "Not Found"
            userAvatarUrl = "https://i.ytimg.com/vi/_3KtqEfHjeQ/maxresdefault.jpg"
        embed.set_author(name=userName,
                         icon_url=userAvatarUrl,
                         url="https://www.hak-leibnitz.at/")
    print("after if")
    valueFach = "\n"
    valueNoten = "\n"
    notenSumme = 0
    anzahlFaecher = 0
    #print(notenPerson)
    for x in notenPerson:
        # print(x[0])
        valueFach += x[0]
        valueFach += "\n"
        valueNoten += x[1]
        valueNoten += "\n"
        if x[1] != "NULL":
           notenSumme += int(x[1])
           anzahlFaecher += 1
    if anzahlFaecher != 0:
    	notenDurchschnitt = round(notenSumme/anzahlFaecher,2)
    else:
        notenDurchschnitt = 0.0
    embed.add_field(value=valueFach, inline=True, name="**Fach**")
    embed.add_field(value=valueNoten, inline=True, name="**Note**")
    embed.add_field(value=notenDurchschnitt, inline=False, name="**Durchschnitt**")
    await ctx.send(embed=embed)


@client.command(brief="<Fach> <Note>", description="Ändert die Note eines speziellen Faches (<Fach> <Note>)")
async def change(ctx, fach, note):
    print(f"change")
    global noten1
    noten1 = SimpleNoten()
    if len(note) == 1 and re.match(r"[1-5]", note):
        noten1.setNote(fach, note, ctx.author.id)
        await noten(ctx)
    else:
        await ctx.send("```Ungültige Eingabe```")


client.run("<your-token>")
