"""
Delete subscriber from Oracle
Input data: Number
"""
from config import Misc
import miscellaneous
import netbox
import json
import sys


def delete_ip_netbox(vrf_name, ip_address):
    vrf_id = netbox.Read().VRFS().get_by_name(vrf_name).get("results")[0].get('id')
    ip = netbox.Read().Addresses().get_by_vrf_id_and_address(vrf_id, ip_address)
    ip_id = ip.get('results')[0].get('id')
    netbox.Delete().Addresses().delete_by_id(ip_id)


def check_vrf(vrf_name):
    vrf = netbox.Read().VRFS().get_by_name(vrf_name).get("results")[0]
    if vrf:
        return {"status": "good", "info": vrf}
    else:
        return {"status": "bad", "info": f"VRF with VRF_NAME = {vrf_name} is not exist"}


def main(data):
    msisdn = data.get("msisdn")
    vrf_name = data.get("vrf_name")
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()

    # get user by msisdn
    user = miscellaneous.Select().Users().username_equals(oracle, cursor, msisdn)

    status = check_vrf(vrf_name)
    if status.get("status") is "bad":
        return {"status": f"bad",
                "error": f"Error with vrf_name",
                "info": status.get("info"),
                "solution": f"Change input vrf_name or create new VRF with VRF_NAME = {vrf_name}"}
    else:
        # if user exist - continue changes
        if user:
            config_id = user[0].get('CONFIG_ID')
            users_in_config = miscellaneous.Select().Users().config_id_equals(oracle, cursor, config_id)

            # if user with this config_id only 1 - delete attributes, else do not delete attributes
            # only delete user from VPN_USERS
            if len(users_in_config) == 1:
                attributes = miscellaneous.Select().Attributes().config_id_equals(oracle, cursor, config_id)
                for attribute in attributes:

                    # if user with static ip, delete ip from netbox
                    if attribute.get("ATT_NAME") == "Framed-IP-Address":
                        ip_address = attribute.get("VALUE")
                        delete_ip_netbox(vrf_name, ip_address)

                    # deleting attributes from VPN_ATTRIBUTES with this config_id
                    miscellaneous.Delete().Attributes().config_id_equals(oracle, connection, cursor, config_id)

            # deleting user from VPN_USERS
            result = miscellaneous.Delete().Users().username_equals(oracle, connection, cursor, msisdn)
            return {"status": "good", "info": result}
        else:
            return {"status": "bad",
                    "error": "Error with Msisdn",
                    "info": "Msisdn do not exist in VPN_USERS or deleted earlier",
                    "solution": "Change input Msisdn"}


if __name__ == '__main__':
    input_data = json.loads(sys.argv[1])
    # input_data = {"msisdn": 375291797391,
    #             "vrf_name": "VPN-BELENERGO"}
    results = main(input_data)
    print(json.dumps(results))