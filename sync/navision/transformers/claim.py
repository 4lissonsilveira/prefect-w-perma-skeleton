from typing import Any

# TODO: not all fields are mandatory, check which ones could be null
def  from_salesforce_to_navision(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "ClaimHeader": {
            "No": claim["CaseNumber"],
            "WarrantyEntryNo": (
                int(claim["Warranty__r"]["Nav_ID__c"])
                if claim["Warranty__r"]["Nav_ID__c"]
                else 0
            ),
            "VIN": claim["Vehicle__r"]["Nav_ID__c"],
            "Make": claim["Vehicle__r"]["Make__c"],
            "Model": claim["Vehicle__r"]["Model__c"],
            "ModelYear": int(claim["Vehicle__r"]["Year__c"]),
            "VehicleOwnerNo": int(claim["Contact"]["NAV_ID__c"]),
            "DealerNo": None,
            "DocumentStorage": None,
            "ClaimStatus": (
                "Unregistered"
                if not claim["Warranty__r"]["Nav_ID__c"] and claim["Unregistered__c"]
                else claim["Status"]
            ),
            "DateClaimReported": claim["Claim_Date__c"],
            "TotalClaimCost": claim["Actual_Invoice_Amount__c"],
            "CustomerFirstName": claim["Contact"]["FirstName"],
            "CustomerLastName": claim["Contact"]["LastName"],
            "CustomerAddress": claim["Contact"]["MailingStreet"],
            "CustomerCity": claim["Contact"]["MailingCity"],
            "CustomerState": claim["Contact"]["MailingState"],
            "CustomerZip": claim["Contact"]["MailingPostalCode"],
            "CustomerCountry": (
                "CA" if claim["Contact"]["MailingCountry"] == "Canada" else "US"
            ),
            "MessageStatus": None,
            "HdrSalesForceID": claim["Id"],
        },
        "ClaimLine": [
            {
                "LineNo": int(claim["Claim_Line__c"]),
                "ProductType": fix_product_type(claim["Product__c"]),
                "ClaimDate": claim["CreatedDate"][:10],
                "DateOfLoss": claim["Date_of_Loss__c"][:10],
                "DatePaid": claim["Posting_Date__c"][:10],
                "InspectionReceivedDate": claim["Inspection_Received_Date__c"][:10],
                "Replaced": claim["Resolution__c"],
                "ClaimDescription": claim["Description"][:250],
                "ClaimDetermination": claim["Claim_Determination__c"],
                "ClaimStatus": fix_claim_status(
                    "List 1"
                    if "safelite" in claim["Technician_Account__r"]["Name"].lower()
                    else (
                        "Processed"
                        if claim["Status"] == "Payables Approval"
                        and claim["Ready_to_Post__c"]
                        else claim["Status"]
                    )
                ),
                "LineSalesForceID": claim["Id"],
            }
        ],
    }


def fix_product_type(product: str) -> str:
    return {
        "Alloy Wheel": "ALLOYW",
        "ClearPlate": "CP",
        "Door Edge Cup Guard": "DECG",
        "Etchguard": "EG",
        "Fiberguard": "FG",
        "Key Replacement": "KEYREP",
        "Leatherguard": "LG",
        "Paintless Dent Repair": "PDR",
        "Paintguard": "PG",
        "Rustguard": "RG",
        "Soundguard": "SG",
        "Tire & Wheel": "TW",
        "Windshield": "WS",
    }.get(product, product)


def fix_claim_status(status: str) -> str:
    return {
        "List 1": "List 1",
        "Processed": "Docs Processed",
        "Payables Approval": "Docs Received",
        "Waiting": "Processing",
        "New": "Processing",
        "Scheduled": "Referred",
        "Payment Process": "Docs Processed",
        "Requires Additional Work": "Further Work",
        "Closed - Paid": "Resolved",
        "Closed - Denied": "Resolved",
        "Closed - Ghost": "Resolved",
        "Closed - FTP": "Resolved",
    }.get(status, status)
