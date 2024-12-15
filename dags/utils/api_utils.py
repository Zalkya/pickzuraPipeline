import os
import requests
from functools import lru_cache


#@lru_cache(maxsize=1)  # Cache a single token
def get_bearer_token(API_BASE_URL, API_CNPJ, API_HASH):
    auth_url = f"{API_BASE_URL}/autenticar"
    payload = {
        "cnpj": API_CNPJ,
        "hash": API_HASH
    }
    headers = {"Content-Type": "application/json"}

    # Prepare the request for inspection
    request = requests.Request("POST", auth_url, json=payload, headers=headers)
    prepared_request = request.prepare()

    # Print the prepared request details
    print("Request URL:", prepared_request.url)
    print("Request Headers:", prepared_request.headers)
    print("Request Body:", prepared_request.body)

    # Send the request
    with requests.Session() as session:
        response = session.send(prepared_request)
        response.raise_for_status()  # Raise an error for bad HTTP responses

    # Parse the response
    token = response.json().get("token")
    if not token:
        raise ValueError("Token not found in response")
    return token



def fetch_data_from_api(api_base_url, token):
    """Fetch data from the API using the bearer token."""
    url = f"{api_base_url}/produtos-data-ultima-alteracao?dataUltimaAlteracaoInicio=2023-01-01&dataUltimaAlteracaoFim=2024-09-24&campoOrdem=PRODUTODES&ordem=ASC&itensPorPagina=10&pagina=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()  # Adjust parsing based on API response
