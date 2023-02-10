import requests
import json


def get_from_ipfs(cid, content_type="json"):
    # get cid and create that and pass object parameter and need to make api call with credentials and cid
    # change str to json object
    # change json to dictionary and then return
   # assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
    # YOUR CODE HERE

    #assert isinstance(data, dict), f"get_from_ipfs should return a dict"


params = ('arg', cid)
response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params,
                         auth=("2LVaqfpTeMvb7NuwrPSBBNvSL2u", "17e2b174612e5eea2af96e5b7f55ebbf"))
return data

files = {
    'file': '<pass>'
}

get_from_ipfs(files)
