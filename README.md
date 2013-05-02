xmpp-bot
========

A framework for writing quick and dirty XMPP chat bots


### Requirements:

sleekxmpp==1.1.11
wsgiref==0.1.2

### Example

```
import urllib2
import json
import logging
from botengine import BaseEngine, XMPPBot

# Logging:
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

# This is where you create your own engine
# For lack of a better word, the engine is where all the logic of the commands are stored.
class MyEngine(BaseEngine):

    def __init__(self):
        BaseEngine.__init__(self)
        
        # This where you register all the commands
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

# This is where you register the engine
bot.register_engine(MyEngine)

bot.connect(('talk.google.com', 5222))
bot.process(block=True)
```

### Running

`$ python example.py`

### TODO

There is still lots of bits to do. This project is not even close to half-way finished.
