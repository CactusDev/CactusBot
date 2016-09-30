from cactusbot.handler import Handlers
from cactusbot.handlers.command import CommandHandler

a = Handlers(CommandHandler())
b = a.handle("message", "potato")
for thing in b:
    print(thing)
