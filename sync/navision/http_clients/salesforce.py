import logging
from typing import Any

from simple_salesforce import Salesforce # type: ignore


logger = logging.getLogger(__name__)


class SalesforceClient:
    def __init__(self, client: Salesforce):
        self.client = client

    def execute_query(self, soql: str) -> list[dict[str, Any]]:
        try:
            return self.client.query(soql).get("records", [])  # type: ignore
        except Exception as exc:
            logger.error("SOQL query failed: %s", exc, exc_info=True)
            raise

    def update_object(self, name:str, id_: str, data: dict[str, str]):
        object = getattr(self.client, name)
        object.update(id_, data)

    # TODO: - Warranty object doesnt exist as standard
    #       - This version of SF doesnt have middlename as a field in contact 
    def get_claims(self, limit: int = 50) -> list[dict[str, Any]]:
        if not isinstance(limit, int): #type: ignore
            raise ValueError("Limit must be an integer")

        query = f"""
            SELECT
                Technician_Account__r.Name,
                Id,
                Actual_Invoice_Amount__c,
                CaseNumber,
                Claim_Date__c,
                Claim_Determination__c,
                Claim_Number__c,
                CreatedDate,
                Date_of_Loss__c,
                Description,
                Inspection_Received_Date__c,
                LastModifiedDate,
                Posting_Date__c,
                Product__c,
                Ready_to_Post__c,
                Resolution__c,
                Status,
                Unregistered__c,
                Approved_Amount__c,
                Claim_Date_Created_Date_Diff__c,
                Claim_Line__c,
                Claim_Header__c,
                Color__c,
                ContactEmail,
                ContactMobile,
                ContactPhone,
                Days_from_Purchase_to_Claim__c,
                Days_from_loss_to_claim__c,
                Days_to_Determine__c,
                Dealer_Amount__c,
                Denial_Reason__c,
                Denial_Reason_Text__c,
                Estimated_Cost__c,
                Invoice_Total__c,
                Nav_Claim_Header_ID__c,
                Permaplate_Amount__c,
                Product_Group__c,
                Purchase_Date__c,
                Retailer_Amount__c,
                Retailer_Group__c,
                Type,
                Vehicle__r.Make__c,
                Vehicle__r.Model__c,
                Vehicle__r.Name,
                Vehicle__r.Nav_ID__c,
                Vehicle__r.Year__c,
                Vehicle__r.NewUsed__c,
                Vehicle__r.Odometer_at_Purchase__c,
                Vehicle__r.Purchase_Date__c,
                Vehicle__r.Trim__c,
                Vehicle__r.Vehicle_Owner__c,
                Contact.FirstName,
                Contact.LastName,
                Contact.MailingCity,
                Contact.MailingCountry,
                Contact.MailingPostalCode,
                Contact.MailingState,
                Contact.MailingStreet,
                Contact.NAV_ID__c,
                Contact.Email,
                Contact.MobilePhone,
                Contact.Name,
                Contact.Phone,
                Warranty__r.Nav_ID__c
            FROM Case
            WHERE Nav_Id__c = null
              AND (
                Status = 'Payment Process'
                OR Status = 'Payables Approval'
                OR (
                    Status = 'Referred'
                    AND Technician_Account__r.Name LIKE '%safelite%'
                )
              )
            ORDER BY LastModifiedDate DESC
            LIMIT {limit}
        """
        return self.execute_query(query)


    # TODO: - Warranty object doesnt exist as standard
    #       - This version of SF doesnt have middlename as a field in contact 
    def get_claim_by_case_number(self, case_number: str) -> dict[str, Any]:
        query = f"""
            SELECT
                Technician_Account__r.Name,
                Id,
                Actual_Invoice_Amount__c,
                CaseNumber,
                Claim_Date__c,
                Claim_Determination__c,
                Claim_Number__c,
                CreatedDate,
                Date_of_Loss__c,
                Description,
                Inspection_Received_Date__c,
                LastModifiedDate,
                Posting_Date__c,
                Product__c,
                Ready_to_Post__c,
                Resolution__c,
                Status,
                Unregistered__c,
                Warranty_Line_Item__c,
                Approved_Amount__c,
                Claim_Date_Created_Date_Diff__c,
                Claim_Line__c,
                Claim_Header__c,
                Color__c,
                ContactEmail,
                ContactMobile,
                ContactPhone,
                Days_from_Purchase_to_Claim__c,
                Days_from_loss_to_claim__c,
                Days_to_Determine__c,
                Dealer_Amount__c,
                Denial_Reason__c,
                Denial_Reason_Text__c,
                Estimated_Cost__c,
                Invoice_Total__c,
                Nav_Claim_Header_ID__c,
                Permaplate_Amount__c,
                Product_Group__c,
                Purchase_Date__c,
                Retailer_Amount__c,
                Retailer_Group__c,
                Type,
                Warranty_Status__c,
                Warranty_Group_Code__c,
                Vehicle__r.Make__c,
                Vehicle__r.Model__c,
                Vehicle__r.Name,
                Vehicle__r.Nav_ID__c,
                Vehicle__r.Year__c,
                Vehicle__r.NewUsed__c,
                Vehicle__r.Odometer_at_Purchase__c,
                Vehicle__r.Purchase_Date__c,
                Vehicle__r.Trim__c,
                Vehicle__r.Vehicle_Owner__c,
                Contact.FirstName,
                Contact.LastName,
                Contact.MailingCity,
                Contact.MailingCountry,
                Contact.MailingPostalCode,
                Contact.MailingState,
                Contact.MailingStreet,
                Contact.NAV_ID__c,
                Contact.Email,
                Contact.MobilePhone,
                Contact.Name,
                Contact.Phone
            FROM Case
            WHERE CaseNumber = '{case_number}'
        """
        return self.execute_query(query)[0]

    def update_claims(self, rows: dict[str, dict[str, str]]):
        [
            self.update_object("Case", id_, data) 
            for id_, data in rows.items()
        ]


def create_salesforce_client(
    domain: str, client_id: str, client_secret: str
) -> SalesforceClient:
    sf_client = Salesforce(
        domain=domain, consumer_key=client_id, consumer_secret=client_secret
    )

    return SalesforceClient(sf_client)
