import pyshorteners

def url_shortener(url: str) -> str:
    '''
    Returns the new shortened link as a string
    '''

    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

