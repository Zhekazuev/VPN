"""
Add new subscriber in Oracle with static IPv4
Input data: Number and Parameters(VRF, POOL, other attributes)
"""
from config import Misc
import miscellaneous
import netbox
import json
import sys


def get_ip_netbox(pool_name):
    prefix = netbox.Read().Prefixes().get_by_name(pool_name).get("results")[0]
    prefix_id = prefix.get("id")
    ip_address = netbox.Read().Addresses().get_free_ips_by_prefix_id(prefix_id)[0]['address']
    return ip_address


def check_config_id(config_id):
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    result = miscellaneous.Select().Attributes().config_id_equals(oracle, cursor, config_id)
    if result:
        return {"status": "bad", "info": result}
    else:
        return {"status": "good", "info": "all good"}


def add_subscriber_oracle(attributes, config_id, msisdn, customer_id, profile_id, password):
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    results = []

    for name, value in attributes.items():
        if name == "Framed-IP-Address" and value == "":
            pool_name = attributes.get("Framed-Pool")
            value = get_ip_netbox(attributes.get(pool_name)).split('/')[0]
            vrf = netbox.Read().Prefixes().get_by_name(pool_name).get('results')[0]
            vrf_id = vrf.get('vrf').get('id')
            tenant_id = vrf.get('tenant').get('id')
            netbox.Create().Addresses().create(address=value, vrf_id=vrf_id, tenant_id=tenant_id,
                                               description='', custom_fields={})
        result = miscellaneous.Insert().Attributes().all(oracle, connection, cursor, value, config_id, name)
        results.append(result[0])

    new_user = miscellaneous.Insert().Users().all(oracle, connection, cursor,
                                                  msisdn, customer_id, config_id, profile_id, password)
    oracle.close(connection, cursor)

    return {"status": "good", "info": {"new_user": new_user, "results": results}}


def main(data):
    msisdn = data.get("msisdn")
    attributes = data.get("attributes")
    config_id = data.get("config_id")
    customer_id = data.get("customer_id")
    profile_id = data.get("profile_id")
    password = data.get("password")

    status = check_config_id(config_id)

    if status.get("status") is "bad":
        return {"status": f"Trouble with config_id",
                "error": f"Attributes with CONFIG_ID = {config_id} is exists",
                "info": status.get("info"),
                "solution": "Change input config_id"}
    else:
        return add_subscriber_oracle(attributes, config_id, msisdn, customer_id, profile_id, password)


if __name__ == '__main__':
    # input_data = json.loads(sys.argv[1])
    input_data = {"msisdn": 375291797391,
                  "attributes": {"SN-VPN-Name": "Gi-1",
                                 "SN1-Rad-APN-Name": "vpn.mpls",
                                 "Framed-IP-Address": "",
                                 "Framed-Pool": "VPN-BELENERGO_2"},
                  "config_id": 78900,
                  "customer_id": 10,
                  "profile_id": 11,
                  "password": ""}
    user = main(input_data)
    print(json.dumps(user))
