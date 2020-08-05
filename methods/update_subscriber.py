"""
Add new subscriber in Oracle with static IPv4
Input data: Number and Parameters(VRF, POOL, other attributes)
"""
from config import Misc
import miscellaneous
import netbox
import json
import sys
import re


def get_ip_netbox(pool_name):
    prefixes = netbox.Read().Prefixes().get_by_name(pool_name)
    if prefixes.get("count") is None:
        return {"status": "error", "message": f"Prefixes named {pool_name} does not exist"}
    try:
        prefix = prefixes.get("results")[0]
    except IndexError as prefix_index_error:
        return {"status": "error", "message": prefix_index_error}
    try:
        prefix_id = prefix.get("id")
    except KeyError as prefix_key_error:
        return {"status": "error", "message": prefix_key_error}
    addresses = netbox.Read().Addresses().get_free_ips_by_prefix_id(prefix_id)
    try:
        address = addresses[0]
    except IndexError as address_index_error:
        return {"status": "error", "message": address_index_error}
    try:
        ip_address = address.get("address")
    except KeyError as address_key_error:
        return {"status": "error", "message": address_key_error}
    return {"status": "good", "address": ip_address}


def check_config_id(config_id):
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    result = miscellaneous.Select().Attributes().config_id_equals(oracle, cursor, config_id)
    if result:
        return {"status": "error", "message": f"The provided config_id {config_id} is already in use: {result}"}
    else:
        return {"status": "good", "info": f"The provided config_id {config_id} is not used"}


def add_subscriber_oracle(attributes, config_id, msisdn, customer_id, profile_id, password):
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    results = []

    for name, value in attributes.items():
        if name == "Framed-IP-Address" and value == "":
            pool_name = attributes.get("Framed-Pool")
            netbox_message = get_ip_netbox(attributes.get(pool_name))
            if netbox_message.get("status") is "error":
                return netbox_message
            try:
                value = netbox_message.get("address").split("/")[0]
            except IndexError:
                return {"status": "error", "message": "Failed to get address from Netbox"}
            prefixes = netbox.Read().Prefixes().get_by_name(pool_name)
            if prefixes.get("count") is None:
                return {"status": "error", "message": f"Prefixes named {pool_name} does not exist"}
            try:
                prefix = prefixes.get('results')[0]
            except IndexError:
                return {"status": "error", "message": f"Failed to get Prefix named {pool_name} from Netbox"}
            try:
                vrf_id = prefix.get('vrf').get('id')
            except KeyError:
                return {"status": "error", "message": f"Failed to get VRF ID from Netbox"}
            try:
                tenant_id = prefix.get('tenant').get('id')
            except KeyError:
                return {"status": "error", "message": f"Failed to get Tenant ID from Netbox"}

            netbox.Create().Addresses().create(address=value, vrf_id=vrf_id, tenant_id=tenant_id,
                                               description='', custom_fields={})
        result = miscellaneous.Insert().Attributes().all(oracle, connection, cursor, value, config_id, name)
        try:
            results.append(result[0])
        except IndexError:
            return {"status": "error", "message": f"Failed to get Row before Inserting Attributes in Misc"}
    new_user = miscellaneous.Insert().Users().all(oracle, connection, cursor,
                                                  msisdn, customer_id, config_id, profile_id, password)
    oracle.close(connection, cursor)
    return {"status": "good", "info": {"new_user": new_user, "results": results}}


def main():
    input_data = {"msisdn": {"old": 375291111111, "new": 375291797391}}
    try:
        input_string = sys.argv[1]
    except IndexError:
        return {"status": "error", "message": "Parameters required"}
    # checking if the passed parameter is correct - need json string
    try:
        input_data = json.loads(input_string)
    except json.decoder.JSONDecodeError as json_error:
        return {"status": "error", "message": str(json_error)}

    # Check old MSISDN
    check_msisdn = re.findall(r"^375\d{9}$", str(input_data.get("msisdn").get("old")))
    if not check_msisdn:
        return {"status": "error", "message": "You must enter an old msisdn or "
                                              "the entered old msisdn is not in a format. Correct format: 375291111111"}
    # Check new MSISDN
    check_msisdn = re.findall(r"^375\d{9}$", str(input_data.get("msisdn").get("new")))
    if not check_msisdn:
        return {"status": "error", "message": "You must enter an new msisdn or "
                                              "the entered new msisdn is not in a format. Correct format: 375291111111"}
    old_msisdn = input_data.get("msisdn").get("old")
    new_msisdn = input_data.get("msisdn").get("new")

    old_status = check_old_msisdn(old_msisdn)
    new_status = check_new_msisdn(new_msisdn)

    if old_status.get("status") is "error":
        return old_status
    if new_status.get("status") is "error":
        return new_status
    else:
        return change_msisdn(old_msisdn, new_msisdn)


if __name__ == '__main__':
    print(main())
