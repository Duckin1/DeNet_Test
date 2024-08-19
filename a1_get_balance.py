from web3 import Web3

# Подключение к RPC-серверу сети Polygon
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com/'))

# Проверка подключения
if not w3.is_connected():
    print("Не удалось подключиться к сети Polygon")
    exit()

# Адрес токена (переводим в формат checksum)
token_address = w3.to_checksum_address('0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0')

erc20_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]

# Создание экземпляра контракта
contract = w3.eth.contract(address=token_address, abi=erc20_abi)

# Функция для получения баланса
def get_balance(address):
    balance = contract.functions.balanceOf(w3.to_checksum_address(address)).call()
    return w3.from_wei(balance, 'ether')

address = '0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d'
balance = get_balance(address)
print(f"Баланс адреса {address}: {balance} TBY")
