from Messages.Auth.LoginMessage import LoginMessage
from Messages.Auth.LoginOkMessage import LoginOkMessage
from Messages.Home.OwnHomeDataMessage import OwnHomeDataMessage

from Messages.PiranhaMessage import PiranhaMessage
from Protocol.Messaging import Messaging
import socket

class MessageManager:
    def __init__(self, messaging: Messaging) -> None:
        self.messaging = messaging

    def receiveMessage(self, message: PiranhaMessage):
        messaegType: int = message.getMessageType()

        if (messaegType == 10101):
            self.onLoginMessage(message)
        else:
            print("Unknown message type: " + str(message.getMessageType()))
                                

    def onLoginMessage(self, loginMessage: LoginMessage):
        print(f"[MessageManager] Logged in! AccountId: {loginMessage.accountId.toString()} PassToken: {loginMessage.passToken} ClientMajorVersion: {loginMessage.clientMajorVersion} ClientBuild: {loginMessage.clientBuild} ResourceSha: {loginMessage.resourceSha}")

        self.messaging.sendMessage(LoginOkMessage())
        
        self.messaging.sendMessage(OwnHomeDataMessage())

