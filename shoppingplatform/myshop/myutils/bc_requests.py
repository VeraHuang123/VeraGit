import json
import requests
from tenacity import retry,wait_exponential,stop_after_attempt

store_hash = "rmz2xgu42d"
base_url = 'https://api.bigcommerce.com/stores'

class BCCustomer:
    def __init__(self):
        self.headers = {
            'X-Auth-Token':'ol999cchp7xq536507sq3pbjia3fi43',
            'Content-Type':'application/json',
            'Accept':'application/json'
        }

    @retry(reraise=True,wait=wait_exponential(multiplier=1,max=60),stop=stop_after_attempt(5))
    def get_a_customer(self,customer_id):
        url = f"{base_url}/{store_hash}/v2/customers/{customer_id}"
        resp = requests.get(url,headers=self.headers)
        if resp.status_code!=200:
            return False
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_all_customers(self):
        url = f"{base_url}/{store_hash}/v2/customers?limit=200"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return False
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def create_a_customer(self,data):

        url = f"{base_url}/{store_hash}/v2/customers"
        resp = requests.post(url, headers=self.headers, json=data)
        if resp.status_code != 201:
            return None
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def delete_a_customer(self, customer_id):
        url = f"{base_url}/{store_hash}/v2/customers/{customer_id}"
        resp = requests.delete(url, headers=self.headers)
        if resp.status_code != 200:
            return False
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def update_a_customer(self, customer_id, data):
        url = f"{base_url}/{store_hash}/v2/customers/{customer_id}"
        resp = requests.put(url, headers=self.headers, json=data)
        return resp.json()

class BCOrder:
    def __init__(self):
        self.headers = {
            'X-Auth-Token': 'ol999cchp7xq536507sq3pbjia3fi43',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_all_order(self):
        url = f"{base_url}/{store_hash}/v2/orders?limit=200"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return False
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_a_order(self, order_id):
        url = f"{base_url}/{store_hash}/v2/orders/{order_id}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return False
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def create_a_order(self, data):
        url = f"{base_url}/{store_hash}/v2/orders"
        resp = requests.post(url, headers=self.headers, json=data)
        if resp.status_code != 201:
            return None
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def update_a_order(self, order_id, data):
        url = f"{base_url}/{store_hash}/v2/orders/{order_id}"
        resp = requests.put(url, headers=self.headers, json=data)
        return resp.json()



