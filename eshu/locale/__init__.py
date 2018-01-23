# this is totally a stub
from .en import EnglishLocale


DefaultLocale = EnglishLocale


def translate(msgid, locale=DefaultLocale):
    return locale.get(msgid, 'No translation for %r' % msgid)
