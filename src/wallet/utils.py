from fastapi import HTTPException
from tronpy import Tron

client = Tron()

def get_wallet_info(address: str):
    try:
        # if not client.to_base58check_address(address):
        #     raise ValueError("Invalid Tron address format")

        account = client.get_account(address)
        resources = client.get_account_resource(address)
        balance = account.get('balance', 0) / 1_000_000
        bandwidth = resources.get('freeNetLimit', 0)
        energy = resources.get('EnergyLimit', 0)

        return {"balance": balance, "bandwidth": bandwidth, "energy": energy}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при получении данных: {str(e)}")
