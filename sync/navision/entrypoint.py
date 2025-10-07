from prefect import flow
from claim import flow_sync_case_object, flow_sync_single_case_object


@flow
def main_flow(salesforce_case_number: str):
    """
    Main Prefect flow for syncing Salesforce cases to Navision.
    
    Args:
        salesforce_case_number: Specific case number to sync from UI (optional)
    """
    
    flow_sync_single_case_object(salesforce_case_number)
    flow_sync_case_object()
