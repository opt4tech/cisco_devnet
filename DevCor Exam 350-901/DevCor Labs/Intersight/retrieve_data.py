from paramters import INTERSIGHT
import requests
import intersight
import re
from intersight.api import compute_api
from pprint import pprint

import intersight
import re


def get_api_client(api_key_id, api_secret_file, endpoint="https://intersight.com"):
    with open(api_secret_file, 'r') as f:
        api_key = f.read()

    if re.search('BEGIN RSA PRIVATE KEY', api_key):
        # API Key v2 format
        signing_algorithm = intersight.signing.ALGORITHM_RSASSA_PKCS1v15
        signing_scheme = intersight.signing.SCHEME_RSA_SHA256
        hash_algorithm = intersight.signing.HASH_SHA256

    elif re.search('BEGIN EC PRIVATE KEY', api_key):
        # API Key v3 format
        signing_algorithm = intersight.signing.ALGORITHM_ECDSA_MODE_DETERMINISTIC_RFC6979
        signing_scheme = intersight.signing.SCHEME_HS2019
        hash_algorithm = intersight.signing.HASH_SHA256

    configuration = intersight.Configuration(
        host=endpoint,
        signing_info=intersight.signing.HttpSigningConfiguration(
            key_id=api_key_id,
            private_key_path=api_secret_file,
            signing_scheme=signing_scheme,
            signing_algorithm=signing_algorithm,
            hash_algorithm=hash_algorithm,
            signed_headers=[
                intersight.signing.HEADER_REQUEST_TARGET,
                intersight.signing.HEADER_HOST,
                intersight.signing.HEADER_DATE,
                intersight.signing.HEADER_DIGEST,
            ]
        )
    )
    
    # if you want to turn off certificate verification
    # configuration.verify_ssl = False

    return intersight.ApiClient(configuration)

def main():
    global base_url

    base_url = INTERSIGHT['HOST']
    api_client = get_api_client(INTERSIGHT['API_KEY'], './api_secret_file')
    print(api_client)
    api_instance = compute_api.ComputeApi(api_client)
    query_selector="Name,Model"
    filter = "Model ne 'UCSC-C240-M5SN' and Name eq 'UCSPE-10-10-20-40-6-3'"
    kwargs = dict(filter=filter, select=query_selector)

    try:
        api_response = api_instance.get_compute_blade_list(**kwargs)
        pprint(api_response)
    except intersight.ApiException as e:
        print("Exception calling alarm list: %s\n" % e)


if __name__ == '__main__':
    main()