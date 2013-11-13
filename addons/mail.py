from core import ircBot, AddonBase
from db import DB
import os,binascii
import ircHelpers

import re

@ircBot.registerAddon()
class Mail(AddonBase):
    def __init__(self):
        self.commandList = {"mail" : self.send_mail, "mymail" : self.get_mail, "delmail" : self.delete_mail }
        self.joinList = [self.notify]

    def send_mail(self, arguments, messageInfo):
        sender = messageInfo['user']
        message = arguments.split(" ", 1)
        recipient = message[0]
        message = message[1]
        id = binascii.b2a_hex(os.urandom(3)).decode()
        dict = { "sender" : sender, "recipient" : recipient, "message" : message.strip("\r"), "id" : id }
        DB().db_add_data("mail", dict)
        ircHelpers.privateMessage(messageInfo["user"], "sent message to %s" % recipient)

    def get_mail(self, arguments, messageInfo):
        recipient = messageInfo["user"]
        data = DB().db_get_data("mail", "recipient", recipient)
        if len(data) == 0:
            ircHelpers.privateMessage(messageInfo["user"], "You have no messages")
        else:
            for tuple in data:
                ircHelpers.privateMessage(tuple[1], "%s says: %s id: %s" % (tuple[0],tuple[2],tuple[3]))

    def delete_mail(self, arguments, messageInfo):
        DB().db_delete_data("mail","id",arguments.strip('\r'),"=")
        ircHelpers.privateMessage(messageInfo["user"], "Deleted message (if available)")
        
    def notify(self, user):
        data = DB().db_get_data("mail", "recipient", user)
        if len(data) != 0:
            ircHelpers.privateMessage(user, "You have mail! You can check it with mymail and delete it with delmail <id>")
