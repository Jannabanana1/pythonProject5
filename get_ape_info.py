@@ -13,45 +13,47 @@
# In general, you can get contract ABIs from etherscan
# https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
# with open('./abi.json', 'r') as f:
    abi = json.load(f)

############################
# Connect to an Ethereum node
api_url = f"https://celo-mainnet.infura.io/v3/ebcd0dee40f2486396df85334c6879b4"  # YOU WILL NEED TO TO PROVIDE THE URL OF AN ETHEREUM NODE
api_url = 'https://mainnet.infura.io/v3/d4e747fdb9574612a0a08497b519e9e8'
provider = HTTPProvider(api_url)
web3 = Web3(provider)


def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID, f"{apeID} must be at least 1"
    assert apeID <= 10000, f"{apeID} must be less than or equal to 10,000"

    data = {'owner': "", 'image': "", 'eyes': ""}

    # YOUR CODE HERE
    contract = web3.eth.contract(address=contract_address, abi=abi)

    # get owner
    owner = contract.functions.ownerOf(apeID).call()

    tokenURI = contract.functions.tokenURI(apeID).call()
    parsed_tokenURI = tokenURI[7:len(tokenURI)]
    cat1 = 'https://ipfs.infura.io:5001/api/v0/cat?arg='
    cat2 = parsed_tokenURI
    concatenated = cat1 + cat2
    response = requests.post(concatenated, auth=('2F8IN6a9C6EGOdvXhJId3AtjNIt', '7cbae92f5fce16d7da2cd221e75c0480'))
    response_data = json.loads(response.text)

    for obj in response_data['attributes']:
        if (obj['trait_type']) == 'Eyes':
            data['eyes'] = obj['value']

    data['owner'] = owner
    endpoint = 'https://gateway.pinata.cloud/ipfs/'

    token_url = contract.functions.tokenURI(apeID).call()

    d = fetch_from_ipfs(token_url);  # returns dictionary
    image = "";
    eyes = "";
    for key, value in d.items():
        if key == 'image':
            image = value
            print(image)
        elif key == 'attributes':
            for item in d[key]:
                if (item['trait_type'] == 'Eyes'):
                    eyes = item['value']
    data['image'] = image
    data['eyes'] = eyes
    data['image'] = response_data['image']

    assert isinstance(data, dict), f'get_ape_info{apeID} should return a dict'
    assert all([a in data.keys() for a in
                ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner','image' and 'eyes'"
    return data

get_ape_info(15)
