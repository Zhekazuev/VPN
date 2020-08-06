"""
Add new subscriber in Oracle with static IPv4
Input data: Number and Parameters(VRF, POOL, other attributes)
"""
from config import Misc
import miscellaneous
import json
import sys
import re


def check_old_msisdn(old_msisdn):
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    users = miscellaneous.Select().Users().username_equals(oracle, cursor, old_msisdn)
    try:
        user = users[0]
    except IndexError:
        return {"status": "error", "message": f"User with msisdn {old_msisdn} does not exist"}
    try:
        user.get('USER_NAME')
    except KeyError as key_error:
        return {"status": "error", "message": key_error}
    return {"status": "good", "message": user.get('USER_NAME')}


def check_new_msisdn(new_msisdn):
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    users = miscellaneous.Select().Users().username_equals(oracle, cursor, new_msisdn)
    try:
        user = users[0]
    except IndexError:
        return {"status": "good", "message": f"User with msisdn {new_msisdn} does not exist"}
    try:
        user.get('USER_NAME')
    except KeyError as key_error:
        return {"status": "good", "message": key_error}
    return {"status": "error", "message": f"User with msisdn {user.get('USER_NAME')} does exist"}


def change_msisdn(old_msisdn, new_msisdn):
    oracle = miscellaneous.OracleDB(host=Misc.ORACLE_IP_TEST)
    connection, cursor = oracle.connect()
    result = miscellaneous.Update().Users().username(oracle, connection, cursor, old_msisdn, new_msisdn)
    return {"status": "good", "message": result}


def main():
    # input_data = {"msisdn": {"old": 375291797391, "new": 375291111111}}
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
