import requests

from spintop import __version__

def spintop_session(user_agent=f'spintop-cli/{__version__}'):
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent})
    return session