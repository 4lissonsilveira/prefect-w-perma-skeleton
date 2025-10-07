from typing import Any

from zeep import Client

class NavisionClient:
    def __init__(self, zeep_client: Client):
        self.client = zeep_client
    
    def insert_update_claim(self, claim_data: dict[str, Any]) -> dict[str, Any]:
        return self.client.service.InsertUpdateClaim( # type: ignore
            claim_data
        )

def create_navision_client():
    #zeep_client = Client("navision_wsdl.xml")
    zeep_client = Client("https://6629d9b4d06c.ngrok-free.app/wsdl")
    return NavisionClient(zeep_client)
