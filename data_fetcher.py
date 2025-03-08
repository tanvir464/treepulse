import requests

def fetch_disease_info(disease_name, lang='en'):
    """
    Fetches a summary of the disease from Wikipedia.
    Use 'bn' for Bangla and 'en' for English.
    """
    endpoint = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{disease_name}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data.get('extract', "No detailed info available.")
    else:
        return "Disease information could not be retrieved."
        
# Example usage:
info_en = fetch_disease_info("Anthracnose", lang='en')
info_bn = fetch_disease_info("অ্যানথ্রাকনোজ", lang='bn')
print("English:", info_en)
print("Bangla:", info_bn)