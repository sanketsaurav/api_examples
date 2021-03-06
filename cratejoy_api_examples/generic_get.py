#!/usr/bin/env python
import requests
import json
import argparse
import time

"""
This command-line utility demonstrates how to do some generic API calls.

It uses a username and password stored in a text file because typing in a
password on the command line makes me sad.

This is mostly useful for quickly pulling a given endpoint to see what it
includes without having to create a new function every time you want to look
at a different endpoint.

Usage: python generic_call.py --endpoint=subscriptions

Examples:
 * python generic_call.py --endpoint=orders/333126707 --subrelations=coupons
     - GETs: https://api.cratejoy.com/v1/orders/333126707?&with=coupons&limit=25&page=1
     - Returns json blob with data for order 333126707, including coupon data.

 * python generic_call.py --endpoint=subscriptions --limit=5 --page=2
     - GETs https://api.cratejoy.com/v1/subscriptions?&limit=5&page=2
     - Returns json blob with data for five subscriptions, starting on page 2.

 * python generic_call.py --endpoint=subscriptions --subrelations=orders,logs --limit=10
     - GETs: https://api.cratejoy.com/v1/subscriptions?&with=orders,logs&limit=10&page=1
     - Returns json blob with data for five subscriptions, including orders and subscription logs.
"""

base_url = 'https://api.cratejoy.com/v1/'
headers = {}
DEBUG = True
session = requests.Session()

def get_auth(client_id='test'):
    for line in open(".credentials"):
        if client_id in line: # Ideally this would user "^client_id "
            return tuple(line.rstrip('\n').split(' '))


def get(endpoint, subrelations=None, limit=25, page=1, print_results=True):
    url = "{}{}?".format(base_url, endpoint)
    if subrelations:
        url = "{}&with={}".format(url, subrelations)
    if limit:
        url = "{}&limit={}".format(url, limit)
    if page:
        url = "{}&page={}".format(url, page)
    print "GET Endpoint: {}\nAS {}\nURL: {}".format(endpoint, auth[0], url)
    start_time = time.time()
    response = requests.get(url, auth=auth, headers=headers)
    end_time = time.time()
    print "Request time: {} seconds".format(end_time - start_time)

    if print_results:
        print "Response:\n{}\n----".format(response.content)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', type=str, help='Endpoint (e.g. "customer")', required=True)
    parser.add_argument('--auth', type=str, help='API client_id', default='test')
    parser.add_argument('--subrelations', type=str, help='Add subrelations (e.g., "coupons" to add "?with=coupons")', default='')
    parser.add_argument('--limit', type=int, help='Value for "limit=###" -- default is 25', default=25)
    parser.add_argument('--page', type=int, help='Value for "page=###" -- default is 1', default=1)
    args = parser.parse_args()

    auth = get_auth(args.auth)

    get(args.endpoint, args.subrelations, args.limit, args.page)
