import requests

def fetch_products_data(
    base_url,
    token,
    start_date,
    end_date,
    order_field="PRODUTODES",
    order="ASC",
    items_per_page=10,
    page=1,
):
    """
    Fetches product data from the API with specified parameters.

    Args:
        base_url (str): The base URL of the API.
        token (str): The Bearer token for authorization.
        start_date (str): Start date for filtering (YYYY-MM-DD).
        end_date (str): End date for filtering (YYYY-MM-DD).
        order_field (str): Field to order results by.
        order (str): Order direction ('ASC' or 'DESC').
        items_per_page (int): Number of items per page.
        page (int): Page number to fetch.

    Returns:
        dict: The response JSON from the API.
    """
    endpoint = f"{base_url}/api/v1/produtos-data-ultima-alteracao"
    params = {
        "dataUltimaAlteracaoInicio": start_date,
        "dataUltimaAlteracaoFim": end_date,
        "campoOrdem": order_field,
        "ordem": order,
        "itensPorPagina": items_per_page,
        "pagina": page,
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad HTTP responses
    return response.json()


"""
# Example usage
if __name__ == "__main__":
    BASE_URL = "https://integracaodshomologacao.useserver.com.br"
    TOKEN = "your_bearer_token_here"
    START_DATE = "2023-01-01"
    END_DATE = "2024-09-24"

    try:
        data = fetch_products_data(
            base_url=BASE_URL,
            token=TOKEN,
            start_date=START_DATE,
            end_date=END_DATE,
            order_field="PRODUTODES",
            order="ASC",
            items_per_page=10,
            page=1,
        )
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
"""