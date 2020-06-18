from io import StringIO
import sys
import time
from contextlib import contextmanager
import threading
import _thread
from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals
from database import send
from main import client

codeOut = StringIO()
context= sys.argv[2]
exec(context)
code = sys.argv[1]

class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

#redefine "dangerous" functions
def eval(*args):
    pass
def compile(*args):
    pass


@contextmanager
def time_limit(seconds, msg=''):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        timer.cancel()

def isevaluable(s):
    try:
        signal.alarm(1)
        exec(s)
        return True
    except:
        return False

def get_eval_error(bad_code):
    try:
        exec(bad_code)
    except Exception as e: return str(e)

try:
    with time_limit(0.3, 'sleep'):
        if isevaluable(code):
            codeOut = StringIO()
            sys.stdout = codeOut 
            byte_code = compile_restricted(code, '<inline>', 'exec')
            exec(byte_code, safe_globals, {})
            sys.stdout = sys.__stdout__
            step3 = codeOut.getvalue()
            codeOut.close()
            print(step3)
        else:
            print(get_eval_error(code))
except TimeoutException as e:
    print("timed out")
    sys.stdout = sys.__stdout__
    codeOut.close()


