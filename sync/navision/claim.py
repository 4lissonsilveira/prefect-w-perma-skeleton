from prefect import flow
# from prefect.logging import get_run_logger

# from .http_clients.salesforce import create_salesforce_client
# from .http_clients.navision import create_navision_client
# from .transformers.claim import from_salesforce_to_navision


@flow(log_prints=True) # type: ignore
def flow_sync_case_object() -> None:
    print('aaaaaa')
    # logger = get_run_logger() # type: ignore
    # sf_client = create_salesforce_client(
    #     "orgfarm-fa4f9b8218-dev-ed.develop.my",  # domain or instance url
    #     "3MVG9rZjd7MXFdLhb._HMnhm1AWRnoV0BYmerX0NeniOwjGnCpLB5V63WpobYGesT7kU.6xZTzWo5FDqHLNs4", # client id
    #     "86B4D3A674F80344FEDE761EEC0DD0DE6073D47736E7F0A4E179553DC172BE30" # client secret
    # )
    # nv_client = create_navision_client()

    # cases = sf_client.get_claims()
    # rows_to_update: dict[str, dict[str, str]] = {}
    # for case in cases:
    #     sf_case = from_salesforce_to_navision(case)
    #     nv_client.insert_update_claim(sf_case)

    #     rows_to_update[case["Id"]] = {
    #         "Nav_Id__c": str(sf_case["ClaimHeader"]["No"]) + str(sf_case["ClaimLine"][0]["LineNo"])
    #     }

    #     logger.info(f"Claim {sf_case['ClaimHeader']['No']} upserted")

    # sf_client.update_claims(rows_to_update)

# @flow(log_prints=True) # type: ignore
# def flow_sync_single_case_object(salesforce_case_number: str) -> None:
#     logger = get_run_logger() # type: ignore

#     sf_client = create_salesforce_client(
#         "orgfarm-fa4f9b8218-dev-ed.develop.my",  # domain or instance url
#         "3MVG9rZjd7MXFdLhb._HMnhm1AWRnoV0BYmerX0NeniOwjGnCpLB5V63WpobYGesT7kU.6xZTzWo5FDqHLNs4", # client id
#         "86B4D3A674F80344FEDE761EEC0DD0DE6073D47736E7F0A4E179553DC172BE30" # client secret
#     )
#     nv_client = create_navision_client()

#     case = sf_client.get_claim_by_case_number(salesforce_case_number)
#     rows_to_update: dict[str, dict[str, str]] = {}

#     sf_case = from_salesforce_to_navision(case)
#     nv_client.insert_update_claim(sf_case)

#     rows_to_update[case["Id"]] = {
#         "Nav_Id__c": str(sf_case["ClaimHeader"]["No"]) + str(sf_case["ClaimLine"][0]["LineNo"])
#     }
#     logger.info(f"Claim {sf_case['ClaimHeader']['No']} upserted")
#     sf_client.update_claims(rows_to_update)
