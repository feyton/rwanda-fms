
import random
from datetime import datetime


def permit_code():
    string = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    randomstr = ''.join((random.choice(string)) for x in range(4))
    return 'H-%s-%s' % (datetime.now().strftime('%y%m%d'), randomstr)
