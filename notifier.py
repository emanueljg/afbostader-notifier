import os
import pickle
import time
import yaml
from pprint import pprint

from plyer import notification

import requests

f = open('config.yaml', 'r')
cfg = yaml.safe_load(f)
f.close()


def save_data(data):
    """Serialize data to PATH."""
    with open(cfg['products_path'], 'wb') as f:
        pickle.dump(data, f)


def load_data():
    """Return either a serialized list from PATH or return an empty list."""
    if os.path.exists(cfg['products_path']):
        with open(cfg['products_path'], 'rb') as f:
            return pickle.load(f)
    else:
        return []

# LOAD PRODUCTS
loaded_products = load_data()
# LOAD PRODUCTS


def get_new_products(all=False):
    """Get all the new products."""
    data = requests.get('https://www.afbostader.se/redimo/rest/vacantproducts?lang=sv_SE&type=1').json()
    products = data['product']
    save_data(products)
    if all:
        return products

    loaded_ids = {loaded_product['productId'] for loaded_product in loaded_products}  # Set comprehension! Hell yeah!
    new_products = [product for product in products if product['productId'] not in loaded_ids]

    return new_products


def send_notifcations(*products):
    """Send notifcations about each product."""
    # CHARMAX TOTAL: 140
    # CHARMAX LINE: 35
    for p in products:
        title = "Ny annons!"
        message = f"{p['address']}\n" \
                  f"{p['shortDescription']} {p['sqrMtrs']}kvm\n" \
                  f"{p['rent']}kr/mån\n" \
                  f"Inflyttningsdatum: {p['moveInDate']}"
        app_name = 'Bostadsannonserare'
        timeout = cfg['timeout']

        notification.notify(title=title, message=message, app_name=app_name, timeout=timeout)
        time.sleep(timeout)


def main():
    """Run the program."""
    run = True
    while run:
        new_products = get_new_products()
        if new_products:
            send_notifcations(*new_products)
        time.sleep(cfg['cooldown'])


if __name__ == '__main__':
    main()


