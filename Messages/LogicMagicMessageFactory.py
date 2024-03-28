from Messages.Auth.LoginMessage import LoginMessage

class LogicMagicMessageFactory:
    messages = {
        10101: LoginMessage,
    }

    def createMessageByType(messageType):
        messages = LogicMagicMessageFactory.messages

        if (messageType in LogicMagicMessageFactory.messages.keys()):
            if (type(messages[messageType]) is None): # if the message type does not exist, pass (return None)
                pass
            else:
                print("[LogicMagicMessageFactory]", str(messageType) + " created")
                return messages[messageType]() # if the message type exists, return a new instance of the message
        else:
            return None