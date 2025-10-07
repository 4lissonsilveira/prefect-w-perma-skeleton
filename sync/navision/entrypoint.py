from prefect import flow
from claim import flow_sync_case_object, flow_sync_single_case_object


@flow(log_prints=True) # type: ignore
def main_flow():
    """
    Main Prefect flow for syncing Salesforce cases to Navision.
    
    Args:
        salesforce_case_number: Specific case number to sync from UI (optional)
    """
    print("flow ok")
    #flow_sync_single_case_object(salesforce_case_number)
    #flow_sync_case_object()
