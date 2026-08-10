import hashlib
import binascii
import datetime
import timeago

salt = b'$#0x--./\\98'


def hash(string):
    value = '' if string is None else str(string)
    dk = hashlib.pbkdf2_hmac('sha256', value.encode('utf-8'), salt, 100000)
    return binascii.hexlify(dk).decode('utf-8')


def b_hash(string):
    value = '' if string is None else str(string)
    dk = hashlib.pbkdf2_hmac('sha256', value.encode('utf-8'), salt, 100000)
    return binascii.hexlify(dk)


def ago(date):
    if date is None:
        return ''
    if isinstance(date, str):
        parsed = None
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'):
            try:
                parsed = datetime.datetime.strptime(date, fmt)
                break
            except ValueError:
                pass
        if parsed is None:
            return ''
        date = parsed
    if not isinstance(date, (datetime.datetime, datetime.timedelta)):
        return ''
    try:
        return timeago.format(date, datetime.datetime.now())
    except Exception:
        return ''
