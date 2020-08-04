"""
Need for working with UNP from GOV.by
"""
import requests
import logging
import urllib3
import json


urllib3.disable_warnings()
logging.captureWarnings(True)


def get_params(unp=200274574):
    url = f"https://www.portal.nalog.gov.by/grp/getData?unp={unp}&charset=UTF-8&type=json"
    response = requests.get(url, verify=False)
    response = json.loads(response.text)
    full_name = response['ROW']['VNAIMP']
    short_name = response['ROW']['VNAIMK']
    address = response['ROW']['VPADRES']
    return {"unp": unp, "full": full_name, "short": short_name, "address": address}


if __name__ == '__main__':
    print(get_params(200274574))
