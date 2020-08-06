"""
Delete subscriber from Oracle
Input data: Number
"""
from config import Misc
import netbox
import miscellaneous
import json
import sys
import re


def delete_ip_netbox(vrf_name, ip_address):
    vrfs = netbox.Read().VRFS().get_by_name(vrf_name)
    if vrfs.get("count") is None:
        return {"status": "error", "message": f"VRF named {vrf_name} does not exist"}
    try:
        vrf = netbox.Read().VRFS().get_by_name(vrf_name).get("results")[0]
    except IndexError as vrf_index_error:
        return {"status": "error", "message": vrf_index_error}
    try:
        vrf_id = vrf.get("id")
    except KeyError as vrf_key_error:
        return {"status": "error", "message": vrf_key_error}
    ips = netbox.Read().Addresses().get_by_vrf_id_and_address(vrf_id, ip_address)
    try:
        ip = ips.get('results')[0]
    except IndexError as ip_index_error:
        return {"status": "error", "message": ip_index_error}
    try:
        ip_id = ip.get('id')
    except KeyError as ip_key_error:
        return {"status": "error", "message": ip_key_error}
    netbox.Delete().Addresses().delete_by_id(ip_id)


def check_vrf(vrf_name):
    vrfs = netbox.Read().VRFS().get_by_name(vrf_name)
    if vrfs.get("count") is None:
        return {"status": "error", "message": f"VRF named {vrf_name} does not exist"}
    try:
        vrf = vrfs.get("results")[0]
    except IndexError:
        return {"status": "error", "message": f"VRF named {vrf_name} does not exist"}
    return {"status": "good", "message": vrf}


def main():
    # input_data = {"msisdn": 375291797391,
    #               "vrf": {"name": "VPN-BELENERGO",
    #                      "rd": 10234}
    #               }
    # checking parameter passing
    try:
        input_string = sys.argv[1]
    except IndexError:
        return {"status": "error", "message": "Parameters required"}
    # checking if the passed parameter is correct - need json string
    try:
        input_data = json.loads(input_string)
    except json.decoder.JSONDecodeError as json_error:
        return {"status": "error", "message": str(json_error)}

    # Check MSISDN
    check_msisdn = re.findall(r"^375\d{9}$", str(input_data.get("msisdn")))
    if not check_msisdn:
        return {"status": "error", "message": "You must enter an msisdn or "
                                              "the entered msisdn is not in a format. Correct format: 375291111111"}
    # Parameter check: VRF
    if input_data.get("vrf") is None:
        return {"status": "error", "message": "You must enter an VRF: 'vrf':{'name': 'VPN-BELENERGO', 'rd': 10234}"}

    # Check VRF Name
    if not isinstance(input_data.get("vrf").get("name"), str):
        return {"status": "error", "message": "The entered VRF Name is not str type"}

    msisdn = input_data.get("msisdn")
    vrf_name = input_data.get("vrf").get("name")
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    # get user by msisdn
    users = miscellaneous.Select().Users().username_equals(oracle, cursor, msisdn)

    vrf_status = check_vrf(vrf_name)
    if vrf_status.get("status") is "error":
        return vrf_status
    else:
        # Check User Existence Check
        try:
            user = users[0]
        except IndexError:
            return {"status": "error", "message": f"User with msisdn {msisdn} does not exist"}
        try:
            config_id = user.get('CONFIG_ID')
        except KeyError as key_error:
            return {"status": "error", "message": key_error}

        # Check user has config_id - continue changes
        if config_id is (None or ""):
            return {"status": "error", "message": f"User with msisdn {msisdn} has no config_id in SQL-request"}

        users_in_config = miscellaneous.Select().Users().config_id_equals(oracle, cursor, config_id)

        # If there is only one user with this config_id - remove attributes, otherwise do not remove attributes
        # (only delete user from VPN_USERS)
        if len(users_in_config) == 1:
            attributes = miscellaneous.Select().Attributes().config_id_equals(oracle, cursor, config_id)
            for attribute in attributes:
                # if user with static ip, delete ip from netbox
                if attribute.get("ATT_NAME") == "Framed-IP-Address":
                    try:
                        ip_address = attribute.get("VALUE")
                        delete_ip_netbox(vrf_name, ip_address)
                    except KeyError:
                        continue
                # deleting attributes from VPN_ATTRIBUTES with this config_id
                miscellaneous.Delete().Attributes().config_id_equals(oracle, connection, cursor, config_id)
        # deleting user from VPN_USERS
        result = miscellaneous.Delete().Users().username_equals(oracle, connection, cursor, msisdn)
        return {"status": "good", "message": result}


if __name__ == '__main__':
    print(main())
