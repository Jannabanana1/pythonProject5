import requests
import json


def pin_to_ipfs(data):
    assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
    #YOUR CODE HERE
    data_str = str(data)
    response = requests.post('https://ipfs.infura.io:5001/api/v0/add',
                             files={'file' : data_str},auth=('2L58AfT67nPxin5ayTe2iHI4Qkg','02e45d5f2415b3b035aa1eb04bdfa1f2'))
    #print(response)
    return_value = response.json()
    cid = return_value['Hash']
    return cid
def get_from_ipfs(cid,content_type="json"):
    assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
    #YOUR CODE HERE
    url = 'https://ipfs.infura.io:5001/api/v0/cat?arg=' + cid
    params = (
    ('arg',cid),
    )
    response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=('2L58AfT67nPxin5ayTe2iHI4Qkg','02e45d5f2415b3b035aa1eb04bdfa1f2'))
    #print(response)
    #print(response.text)
    data = eval(response.text)
    assert isinstance(data,dict), f"get_from_ipfs should return a dict"
    return data








