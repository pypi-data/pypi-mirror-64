from getrails.duckduckgo.search import go_duck
from getrails.google.search import go_gle
from getrails.torch.search import go_onion
from urllib import error

def search (query):
    try:
        result = go_gle(query)
    except error.HTTPError:
        result = go_duck(query)

    result = result.append(go_onion(query))
    return result
