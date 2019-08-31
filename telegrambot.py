import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
from secretkey import TOKEN
import pexpect
from multiprocessing import Process


"""
$ python3.5 countera.py <token>
Counts number of messages a user has sent. Starts over if silent for 10 seconds.
Illustrates the basic usage of `DelegateBot` and `ChatHandler`.
"""

class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self.state = 'command'
        self._message1=''
        self._background='0,0,0'
        self._text='255,0,0'
        self._count=0
        self.processed=0
        self.proc='here'

    async def on_chat_message(self, msg):
        typedmessage=msg['text']
        command = msg['text'].strip().lower()
        if self.state=='command':
            if command=='/set':
                if self.processed==1:
                    self.proc.terminate()
                    self.processed=0
                self.state='message'
                self._count=2
                message='set message'
                await self.sender.sendMessage(message)
            elif command=='/textcolour':
                self.state='color'
                message='set text color'
                await self.sender.sendMessage(message)
            elif command=='/backgroundcolor':
                self.state='bgcolor'
            elif command=='/killall':
                self.proc.terminate()
        elif self.state=='message':
            if self._count==2:
                message='please type next line'
                self._count=1
                self._message1=typedmessage
                await self.sender.sendMessage(message)
            elif self._count==1:
                self.proc =Process(target=creatergb, args=(self._message1,typedmessage,self._text,self._background))
                self.proc.start()
                self.processed=1
                message='done'
                self._count=0
                self.state='command'
                await self.sender.sendMessage(message)
        elif self.state=='color':

                message='color set'
                self._text=typedmessage
                self.state='command'
                await self.sender.sendMessage(message)

        elif self.state=='bgcolor':
            message='background color set'
            self._text=typedmessage
            self.state='command'

            await self.sender.sendMessage(message)

        else:
            message='wrong input'
            await self.sender.sendMessage(message)




def  creatergb(words,words2,textcolor,backgroundcolor):
    child = pexpect.spawn('bash')
    child.expect(r'\$')
    child.sendline('cd /home/Keith/Desktop/rpi-rgb-led-matrix/examples-api-use')
    child.expect(r'\$')
    child.sendline('sudo ./text-example -C {} -B {} -f ../fonts/8x13.bdf --led-no-hardware-pulse --led-rows=32 --led-cols=64 --led-slowdown-gpio=2 --led-chain=2'.format(str(textcolor),str(backgroundcolor)))
    child.expect('Enter')
    child.sendline(words.encode())
    child.expect('')
    child.sendline(words2.encode())
    child.wait()




try:
    bot = telepot.aio.DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, MessageCounter,timeout=30*60),
    ])

    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot).run_forever())
    print('Listening ...')

    loop.run_forever()
except:
    pass
finally:
    proc.terminate()
