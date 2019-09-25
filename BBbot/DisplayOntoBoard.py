import pexpect

def creatergb(words,words2,textcolor,backgroundcolor):
    child = pexpect.spawn('bash')
    child.expect(r'\$')
    # THIS ONE MUST CHANGE ACCORDINGLY
    child.sendline('cd /home/Keith/Desktop/rpi-rgb-led-matrix/examples-api-use') # Edit this accordingly
    child.expect(r'\$')
    child.sendline('sudo ./text-example -C {} -B {} -f ../fonts/8x13.bdf --led-no-hardware-pulse --led-rows=32 --led-cols=64 --led-slowdown-gpio=2 --led-chain=2'.format(str(textcolor),str(backgroundcolor))) # Can play with this
    child.expect('Enter')
    child.sendline(words.encode())
    child.expect('')
    child.sendline(words2.encode())
    child.wait()



class callingRGB:
    def __init__(self, *args, **kwargs):
        self._background = '0,0,0' # Black background default
        self._text = '255,0,0' # Red text color default

    def callrgb(self, words):
        creatergb(words, words, self._text, self._background)