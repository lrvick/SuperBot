import random
def nickColor(nick):#weechat colors
    return ["{C10}","{C13}","{C3}","{C7}","{B}{C2}","{C0}","{B}{C10}","{B}{C6}","{B}{C3}","{C2}"][sum(map(ord,nick))%10]

def colorFilter(msg):
    msg = msg.encode("utf-8")
    replace={
        "{}":chr(15),
        "{LINK}":chr(31)+chr(3)+"2\02\02",
        "{B}":chr(2),
        "{U}":chr(31),
        "{C}":chr(3)+"\02\02"}
    for i in range(16):
        replace["{C%i}"%i]=chr(3)+("%i\02\02"%i)

    for key in replace:
        msg = msg.replace(key,replace[key])
    return msg
def on_unload(bot):
    bot.say = bot.oldSay
    bot.msg = bot.oldMsg

def on_load(bot):
    bot.oldSay=bot.say
    nsay=lambda chan,msg,len=None:bot.oldSay(chan,colorFilter(msg),len)
    setattr(bot,"say",nsay)
    bot.nickColor = nickColor
    #print "bot.msg:",bot.msg 
    bot.oldMsg=bot.msg
    nmsg=lambda user,message,len=None:bot.oldMsg(user,colorFilter(message),len)
    setattr(bot,"msg",nmsg)

def target(bot,sender,room):
    if type(room)==list:
        room=room[0]
    if bot.nickname==room:
        return sender.split("!")[0]
    return room

def on_PRIVMSG(bot,sender,args):
    to = target(bot,sender,args)

    if args[1]=="!colors":
        out = ""
        for i in range(16):
            out +=" {C"+str(i)+"}C"+str(i)
        bot.say(to,out)
    if args[1].startswith("!repeat "):
        msg = args[1]
        msg = msg.replace("!repeat ","")
        bot.msg(to,msg)

    if args[1].startswith("!gayify "):
        msg = args[1]
        msg = msg[8:]
        out = ""
        for c in msg:
            out += "{C"+str(random.randint(2,13))+"}"+c
        bot.msg(to,out)
