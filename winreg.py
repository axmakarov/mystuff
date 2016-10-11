import _winreg
import sys

def find_funky_mimetype():
    default_encoding = sys.getdefaultencoding()
    with _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,
                         r'MIME\Database\Content Type') as mimedb:
        i = 0
        while 1:
            try:
                ctype = _winreg.EnumKey(mimedb, i)
            except EnvironmentError:
                break
            print 'testing:', `ctype`,
            try:
                ctype = ctype.encode(default_encoding) # omit in 3.x!
            except UnicodeEncodeError:
                print 'expected failure'
            except Exception as e:
                print 'unexpected failure:', e
            else:
                print 'ok.'
            i += 1


if __name__ == "__main__":
    find_funky_mimetype()