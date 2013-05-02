from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class XMPPBot(ClientXMPP):

    def __init__(self, jid, password, room=None, nick=None):
        ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        self.engine = BaseEngine

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # XMPP Ping

        self.add_event_handler("session_start", self.session_start) 
        self.add_event_handler("message", self.message) 
        self.add_event_handler("groupchat_invite", self.group_invite) 
        self.add_event_handler("groupchat_message", self.group_message) 
        self.add_event_handler("groupchat_direct_invite", self.group_direct_invite) 
        
        if room is not None and nick is not None:
            self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

        #TODO: Sort out MUC.
        if self.room is not None and self.nick is not None:
            self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)  # If a room password is needed, use: password=the_room_password

    #TODO: Not sure why this is here. This logic should be in the constructor
    def register_engine(self, engine):
        self.engine = engine

    def muc_online(self, presence):
        #if presence['muc']['nick'] != self.nick:
        #    self.send_message(mto=presence['from'].bare, mbody="Hello, %s %s" % (presence['muc']['role'], presence['muc']['nick']), mtype='groupchat')
        pass

    def group_message( self, mesg):
        #if mesg['mucnick'] != self.nick and self.nick in mesg['body']:
        #    self.send_message(mto=mesg['from'].bare, mbody="I heard that, %s." % mesg['mucnick'], mtype='groupchat')
        pass

    def group_invite( self, event):
        pass

    def group_direct_invite( self, event):
        pass

    def message(self, mesg):
        #TODO: Proper exception/error handling
        #TODO: Implement logging

        if mesg['type'] in ( 'chat', 'normal', ):
            try:
                engine = self.engine()
                mesg.reply( engine.respond(mesg) ).send()
            except:
                mesg.reply( "The bot engine is having trouble." ).send()

class BaseEngine:

    def __init__(self):
        self.commands = {
                '_default': {
                    'method': self._default,
                    'help': None },
                'help': {
                    'method': self.help,
                    'help': 'Displays help on commands' },
                }

    def get_opts(self, mesg, optc):
        opts = mesg['body'].split()[1:1+optc]
        return opts

    def register_command(self, command, method, help_txt=''):
        self.commands[command] = { 'method': method, 'help': help_txt }

    def help(self, mesg):
        args = mesg['body'].lower().split()[1:]

        if len(args) < 1:
            commands = ''
            for cmd in self.commands:
                commands = "%s%s - %s\n" % (commands, cmd, self.commands[cmd]['help'])
            return "Here are the commands I understand:\n%s" % commands
        else:
            if args[0] in self.command:
                return "%s - %s\n" % (args[0], self.commands[cmd]['help'])
            else:
                return "I don't know that command, sorry."
		return "Something went wrong"

    def respond( self, mesg ):
        verb = '_default'
        if mesg['type'] in ( 'chat', 'normal', ):
            try:
                verb = mesg['body'].lower().split()[0]
            except:
                pass

        if verb not in self.commands:
            verb = '_default'

        return self.commands[verb]['method'](mesg)

    def _default( self, mesg ):
        # Maybe we should just keep quiet?
        return "I'm not sure I know what to do."
