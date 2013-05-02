
import urllib2
import json
import logging
from botengine import BaseEngine, XMPPBot

# Logging:
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

class MyEngine(BaseEngine):

    def __init__(self):
        BaseEngine.__init__(self)
        self.register_command('hello', self.hello, help_txt='Greetings :)')
        self.register_command('verb', self.verbose, help_txt='Print everything')
        self.register_command('xrate', self.xrate, help_txt='Exchange Rates')

    def hello(self, mesg):
        return "Hello %s" % mesg['from']

    def verbose(self,mesg):
        return str(mesg)

    def xrate(self, mesg):
        curr_from, curr_to = self.get_opts(mesg, 2)
        url = 'http://rate-exchange.appspot.com/currency?from=%s&to=%s' % (curr_from, curr_to)

        try:
            f = urllib2.urlopen(url)
            rate = json.loads(f.read())
        except:
            return "Problems!! Can't connect to currency converter :-("

        if 'rate' in rate:
            return "{0} => {1} {2: f}".format(curr_from, curr_to, rate['rate'])
        else:
            return "There was an error. No rate for you."

bot = XMPPBot( 'bot@kode.co.za', 'P#s5W#0rD!' )
bot.register_engine(MyEngine)
bot.connect(('talk.google.com', 5222))
bot.process(block=True)

