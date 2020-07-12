import os
import pickle
import time
import yaml

from plyer import notification

import requests

with open('config.yaml', 'r') as config:
    cfg = yaml.safe_load(config)


def save_listing(listing):
    """Save listing to `cfg['listing_path']` as specified in `config.yaml`."""
    with open(cfg['listing_path'], 'wb') as f:
        pickle.dump(listing, f)


def load_listing():
    """Return either a loaded listing from `cfg['listing_path']` or an empty list."""
    if os.path.exists(cfg['listing_path']):
        with open(cfg['listing_path'], 'rb') as f:
            return pickle.load(f)
    else:
        return []


def get_new_listing(old_listing):
    """Get the new listing."""
    try:
        fetched_listing = requests.get(cfg['api_url']).json()['product']
    except requests.exceptions.RequestException:
        return old_listing
    else:
        old_item_ids = {old_item['productId'] for old_item in old_listing}
        new_listing = [fetched_item for fetched_item in fetched_listing if
                       fetched_item['productId'] not in old_item_ids]

        if new_listing:
            save_listing(new_listing)

        return new_listing


def send_notifcations(*items):
    """Send notifications for each item, unpacked from a listing."""
    # CHARMAX TOTAL: 140
    # CHARMAX LINE: 35
    for i in items:
        title = "Ny annons!"
        message = f"{i['address']}\n" \
                  f"{i['shortDescription']} {i['sqrMtrs']}kvm\n" \
                  f"{i['rent']}kr/mån\n" \
                  f"Inflyttningsdatum: {i['moveInDate']}"
        app_name = 'Bostadsannonserare'
        app_icon = 'building.ico' if os.path.dirname(os.getcwd()) == 'notifier' else r'notifier-program\notifier\building.ico'

        timeout = cfg['timeout']

        notification.notify(title=title, message=message, app_name=app_name, app_icon=app_icon, timeout=timeout)
        time.sleep(timeout)


def main():
    return
    """Run the program."""
    run = True
    listing = load_listing()
    while run:
        new_listing = get_new_listing(old_listing=listing)
        if new_listing:
            send_notifcations(*new_listing)
            listing = new_listing
        time.sleep(cfg['cooldown'])


if __name__ == '__main__':
    main()


