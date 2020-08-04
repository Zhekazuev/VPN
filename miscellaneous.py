"""
Methods need to work with Oracle DB(misc)

oracle = OracleDB()
connection, cursor = oracle.connect()

#This is space for you query's.
#For example:
all = Select().Dictionary().all(oracle, cursor))

oracle.close(connection, cursor)
"""
from datetime import datetime
import cx_Oracle as Oracle
from config import Misc


class OracleDB:
    """
        Oracle database connection wrapper
        @author: jbaranski
        https://gist.github.com/jbaranski/6537b4075873984ea06e5fbe291f4441
    """
    def __init__(self, host=Misc.ORACLE_IP, port=Misc.ORACLE_PORT, username=Misc.ORACLE_USER,
                 password=Misc.ORACLE_PASS, database=Misc.ORACLE_DB_NAME):
        self.connection = None
        self.cursor = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        """Connect to MISC"""
        try:
            connection = Oracle.connect(f"{self.username}/{self.password}@{self.host}:{self.port}/"
                                        f"{self.database}", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            #print("Connection successfully")
            return connection, cursor
        except Oracle.DatabaseError as e:
            print("There is a problem with Oracle", e)

    @staticmethod
    def make_dictionary_results(cursor):
        """Remake a tuple-answer to dictionary-answer
        Tuple-answer
        [(1, 1, 'Test', 'static', 1000)]
        Dictionary-answer
        [{'CUSTOMER_ID': 1, 'PROFILE_ID': 1, 'PROFILE_NAME': 'Test', 'PROFILE_TYPE': 'static', 'CONFIG_ID': 1000}]
        """
        cursor.rowfactory = lambda *args: dict(zip([d[0] for d in cursor.description], args))
        result = cursor.fetchall()
        return result

    @staticmethod
    def close(connection, cursor):
        """Close connection and cursor"""
        try:
            cursor.close()
            connection.close()
            #print("Disconnection successfully")
        except Oracle.DatabaseError:
            pass


class Select:
    @staticmethod
    def get_by_query(oracle, cursor, query=f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID=1"):
        """Input manually query
        SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID=1'"""
        cursor.execute(query)
        result = oracle.make_dictionary_results(cursor)
        return result

    class Customers:
        @staticmethod
        def all(oracle, cursor):
            """SELECT * FROM SDP.VPN_CUSTOMERS"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def cid_equals(oracle, cursor, cid=0):
            """SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID=0"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={cid}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def unp_equals(oracle, cursor, unp=0):
            """SELECT * FROM SDP.VPN_CUSTOMERS WHERE UNP=0"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE UNP={unp}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def name_equals(oracle, cursor, name='Тестовый абонент'):
            """SELECT * FROM SDP.VPN_CUSTOMERS WHERE NAME='Тестовый абонент'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE NAME='{name}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def name_like(oracle, cursor, name='Тестовый абонент'):
            """SELECT * FROM SDP.VPN_CUSTOMERS WHERE NAME LIKE 'Тестовый абонент'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE NAME LIKE '%{name}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Profiles:
        @staticmethod
        def all(oracle, cursor):
            """SELECT * FROM SDP.VPN_PROFILES"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES ORDER BY CUSTOMER_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def customer_id_equals(oracle, cursor, customer_id=0):
            """SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID=0"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID={customer_id} ORDER BY PROFILE_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_id_equals(oracle, cursor, profile_id=0):
            """SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID=0"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_name_equals(oracle, cursor, profile_name='MinskTrans IoT'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_NAME='MinskTrans IOT'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_NAME='{profile_name}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_name_like(oracle, cursor, profile_name='MinskTrans'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_NAME LIKE '%MinskTrans%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_NAME LIKE '{profile_name}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_type_equals(oracle, cursor, profile_type='static'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_TYPE='static'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_TYPE='{profile_type}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_type_like(oracle, cursor, profile_type='static'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_TYPE LIKE '%static%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_TYPE LIKE '%{profile_type}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def config_id_equals(oracle, cursor, config_id=0):
            """SELECT * FROM SDP.VPN_PROFILES WHERE CONFIG_ID=0'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CONFIG_ID={config_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Dictionary:
        @staticmethod
        def all(oracle, cursor):
            """SELECT * FROM SDP.VPN_DICT ORDER BY CUSTOMER_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_DICT ORDER BY CUSTOMER_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def customer_id_equals(oracle, cursor, customer_id=0):
            """SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID=0 ORDER BY PROFILE_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID={customer_id} ORDER BY PROFILE_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_id_equals(oracle, cursor, profile_id=0):
            """SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID=0"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def attribute_name_equals(oracle, cursor, attribute_name='default'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_NAME='Name'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_NAME='{attribute_name}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def attribute_name_like(oracle, cursor, attribute_name='default'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_NAME LIKE '%Name%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_NAME LIKE '%{attribute_name}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def attribute_value_equals(oracle, cursor, attribute_value='default'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_VALUE='Value'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_VALUE='{attribute_value}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def attribute_value_like(oracle, cursor, attribute_value='default'):
            """SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_VALUE LIKE '%Name%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE ATTRIBUTE_VALUE LIKE '%{attribute_value}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Attributes:
        @staticmethod
        def all(oracle, cursor):
            """SELECT * FROM SDP.VPN_ATTRIBUTES"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES ORDER BY CONFIG_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def value_equals(oracle, cursor, value):
            """SELECT * FROM SDP.VPN_ATTRIBUTES WHERE VALUE='Gi-1'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE VALUE='{value}' ORDER BY CONFIG_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def value_like(oracle, cursor, value):
            """SELECT * FROM SDP.VPN_ATTRIBUTES WHERE VALUE LIKE '%Gi-1%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE VALUE LIKE '%{value}%' ORDER BY CONFIG_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def config_id_equals(oracle, cursor, config_id):
            """SELECT * FROM SDP.VPN_ATTRIBUTES WHERE CONFIG_ID=1"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE CONFIG_ID={config_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def att_id_equals(oracle, cursor, att_id):
            """SELECT * FROM SDP.VPN_ATTRIBUTES WHERE ATT_ID=1"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE ATT_ID={att_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def att_name_equals(oracle, cursor, att_name):
            """SELECT * FROM SDP.VPN_ATTRIBUTES WHERE ATT_NAME='Framed-Pool'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE ATT_NAME='{att_name}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def att_name_like(oracle, cursor, att_name):
            """SELECT * FROM SDP.VPN_ATTRIBUTES WHERE ATT_NAME LIKE '%Framed-Pool%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE ATT_NAME LIKE '%{att_name}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def config_id_and_att_name_equals(oracle, cursor, config_id=1, att_name=''):
            """SELECT * FROM SDP.VPN_ATTRIBUTES WHERE CONFIG_ID=1 AND ATT_NAME='Framed-IP-Address'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES "
                           f"WHERE CONFIG_ID={config_id} AND ATT_NAME='{att_name}'")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Users:
        @staticmethod
        def all(oracle, cursor, ):
            """SELECT * FROM SDP.VPN_USERS"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS ORDER BY CUSTOMER_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def username_equals(oracle, cursor, username='375292222222'):
            """SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='375292222222'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def username_like(oracle, cursor, username='3752922711'):
            """SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='%3752922711%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME LIKE '%{username}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def password_equals(oracle, cursor, password='002pass'):
            """SELECT * FROM SDP.VPN_USERS WHERE PASSWORD='002pass'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PASSWORD='{password}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def password_like(oracle, cursor, password='pass'):
            """SELECT * FROM SDP.VPN_USERS WHERE PASSWORD LIKE '%pass%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PASSWORD LIKE '%{password}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def customer_id_equals(oracle, cursor, customer_id=1):
            """SELECT * FROM SDP.VPN_USERS WHERE CUSTOMER_ID=1"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE CUSTOMER_ID={customer_id} ORDER BY PROFILE_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def config_id_equals(oracle, cursor, config_id=1):
            """SELECT * FROM SDP.VPN_USERS WHERE CONFIG_ID=1"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE CONFIG_ID={config_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_id_equals(oracle, cursor, profile_id=1):
            """SELECT * FROM SDP.VPN_USERS WHERE PROFILE_ID=1"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PROFILE_ID={profile_id} ORDER BY CONFIG_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def profile_id_and_config_id_equals(oracle, cursor, profile_id=1, config_id=1):
            """SELECT * FROM SDP.VPN_USERS WHERE PROFILE_ID=1"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PROFILE_ID={profile_id} AND CONFIG_ID={config_id}"
                           f"ORDER BY CONFIG_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Contexts:
        @staticmethod
        def all(oracle, cursor):
            """SELECT * FROM SDP.VPN_CONTEXTS ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS ORDER BY CONTEXT_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def context_id_equals(oracle, cursor, context_id=0):
            """SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID=1 ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def context_equals(oracle, cursor, context='Gi-1'):
            """SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID=1 ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def context_like(oracle, cursor, context='Gi-1'):
            """SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID=1 ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT LIKE '%{context}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def vrf_count_equals(oracle, cursor, vrf_count=255):
            """SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID=1 ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE VRF_COUNT={vrf_count}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def full_equals(oracle, cursor, is_full=0):
            """SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID=1 ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE IS_FULL={is_full}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class VRFs:
        @staticmethod
        def all(oracle, cursor):
            """SELECT * FROM SDP.VPN_VRFS ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS ORDER BY CONTEXT_ID")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def context_id_equals(oracle, cursor, context_id=0):
            """SELECT * FROM SDP.VPN_VRFS WHERE CONTEXT_ID=1 ORDER BY CONTEXT_ID"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE CONTEXT_ID={context_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def rt_vrf_equals(oracle, cursor, rt_vrf=0):
            """SELECT * FROM SDP.VPN_VRFS WHERE RT_VRF=1"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT_VRF={rt_vrf}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def vrf_name_equals(oracle, cursor, vrf_name='10000_kgb'):
            """SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME='10000_kgb'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME='{vrf_name}'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def vrf_name_like(oracle, cursor, vrf_name='10000_kgb'):
            """SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME LIKE '%10000_kgb%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME LIKE '%{vrf_name}%'")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def rd_equals(oracle, cursor, rd=10000):
            """SELECT * FROM SDP.VPN_VRFS WHERE RD=10000"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RD={rd}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def rt_equals(oracle, cursor, rt='10000'):
            """SELECT * FROM SDP.VPN_VRFS WHERE RT=10000"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT={rt}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def rt_like(oracle, cursor, rt='10000'):
            """SELECT * FROM SDP.VPN_VRFS WHERE RT LIKE '%10000%'"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT LIKE '%{rt}%'")
            result = oracle.make_dictionary_results(cursor)
            return result


class Insert:
    @staticmethod
    def insert_by_query(connection, cursor, query=f"INSERT INTO SDP.VPN_CUSTOMERS "
                                                  f"(CID, NAME, IS_TEST) VALUES (0, 'Name_test', 1)"):
        """Input manually query
        SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID=1"""
        cursor.execute(query)
        connection.commit()
        return cursor

    class Customers:
        @staticmethod
        def all(oracle, connection, cursor, cid, unp, name, address, url='', contact_name='', contact_info='',
                is_test=0):
            """"INSERT INTO SDP.VPN_CUSTOMERS
            (CID, UNP, NAME, ADDRESS, URL, CONTACT_NAME, CONTACT_INFO, ACTIVATION_DATE, IS_TEST)
            VALUES
            (0, 0, 'Name_test', '', '', '', '', to_date('2020-05-20 14:02:46', 'yyyy-mm-dd hh24:mi:ss'), 1);"""
            activation_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"INSERT INTO SDP.VPN_CUSTOMERS "
                           f"(CID, UNP, NAME, ADDRESS, URL, CONTACT_NAME, CONTACT_INFO, ACTIVATION_DATE, IS_TEST) "
                           f"VALUES "
                           f"({cid}, {unp}, '{name}', '{address}', '{url}', '{contact_name}', '{contact_info}', "
                           f"to_date('{activation_date}', 'yyyy-mm-dd hh24:mi:ss'), {is_test})")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={cid}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def minimal(oracle, connection, cursor, cid, unp, name, is_test=0):
            """INSERT INTO SDP.VPN_CUSTOMERS
            (CID, UNP, NAME, ADDRESS, URL, CONTACT_NAME, CONTACT_INFO, ACTIVATION_DATE, IS_TEST)
            VALUES
            (0, 0, 'Name_test', '', '', '', '', to_date('2020-05-20 14:02:46', 'yyyy-mm-dd hh24:mi:ss'), 1);"""
            activation_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"INSERT INTO SDP.VPN_CUSTOMERS "
                           f"(CID, UNP, NAME, ADDRESS, URL, CONTACT_NAME, CONTACT_INFO, ACTIVATION_DATE, IS_TEST) "
                           f"VALUES "
                           f"({cid}, {unp}, '{name}', '', '', '', '', "
                           f"to_date('{activation_date}', 'yyyy-mm-dd hh24:mi:ss'), {is_test})")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={cid}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Profiles:
        @staticmethod
        def all(oracle, connection, cursor, customer_id, profile_id, profile_name, config_id, profile_type='static'):
            """"""
            cursor.execute(f"INSERT INTO SDP.VPN_PROFILES "
                           f"(CUSTOMER_ID, PROFILE_ID, PROFILE_NAME, PROFILE_TYPE, CONFIG_ID) "
                           f"VALUES "
                           f"({customer_id}, {profile_id}, '{profile_name}', '{profile_type}', {config_id})")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

        @staticmethod
        def minimal(oracle, connection, cursor, profile_id, profile_name, config_id, profile_type='static'):
            """"""
            cursor.execute(f"INSERT INTO SDP.VPN_PROFILES "
                           f"(CUSTOMER_ID, PROFILE_ID, PROFILE_NAME, PROFILE_TYPE, CONFIG_ID) "
                           f"VALUES "
                           f"(0, {profile_id}, '{profile_name}', '{profile_type}', {config_id})")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID={profile_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Dictionary:
        @staticmethod
        def all(oracle, connection, cursor, customer_id, profile_id, attribute_name, attribute_value):
            """INSERT INTO SDP.VPN_ATTRIBUTES (VALUE, CONFIG_ID, ATT_ID, ATT_NAME)
            VALUES ('', 1, 3, 'SN-VPN')

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param customer_id: 1
            :param profile_id: 1
            :param attribute_name: 'SN-VPN'
            :param profile_type: 'static'
            :type customer_id: int
            :type config_id: int
            :type att_name: str
            :type value: str


            Returns:
            :return: [{Select before delete}] or {"error": "Error text"}
            :rtype: list"""
            cursor.execute(f"INSERT INTO SDP.VPN_DICT "
                           f"(CUSTOMER_ID, PROFILE_ID, ATTRIBUTE_NAME, ATTRIBUTE_VALUE) "
                           f"VALUES "
                           f"({customer_id}, {profile_id}, '{attribute_name}', '{attribute_value}')")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_DICT WHERE PROFILE_ID={profile_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Attributes:
        @staticmethod
        def all(oracle, connection, cursor, value, config_id, att_name):
            """INSERT INTO SDP.VPN_ATTRIBUTES (VALUE, CONFIG_ID, ATT_ID, ATT_NAME)
            VALUES ('', 1, 3, 'SN-VPN')

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param value: ''
            :param config_id: 1
            :param att_name: 'SN-VPN'
            :type value: str
            :type config_id: int
            :type att_name: str

            Returns:
            :return: [{Select before delete}] or {"error": "Error text"}
            :rtype: list"""
            att_id = cursor.execute(f"SELECT ID FROM SDP.VPN_ATTRIBUTE_DIC WHERE NAME='{att_name}'").fetchall()
            try:
                cursor.execute(f"INSERT INTO SDP.VPN_ATTRIBUTES (VALUE, CONFIG_ID, ATT_ID, ATT_NAME) "
                               f"VALUES ('{value}', {config_id}, {att_id[0][0]}, '{att_name}')")
            except IndexError as e:
                return {"error": f"Error: {e}: with att_id={att_id}"}
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES "
                           f"WHERE VALUE='{value}' AND CONFIG_ID={config_id} AND ATT_ID={att_id[0][0]}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Users:
        @staticmethod
        def all(oracle, connection, cursor, msisdn, customer_id, config_id, profile_id, password=''):
            """INSERT INTO SDP.VPN_USERS (USER_NAME, PASSWORD, CUSTOMER_ID, CONFIG_ID, PROFILE_ID)
            VALUES ('375291234567', '', 1, 1, 1)

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param msisdn: '375291234567'
            :param customer_id: 1
            :param config_id: 1
            :param profile_id: 1
            :param password: '12345qwerty'
            :type msisdn: str
            :type customer_id: int
            :type config_id: int
            :type profile_id: int
            :type password: str


            Returns:
            :return: [{Select before delete}]
            :rtype: list"""
            if type(msisdn) is not str:
                msisdn = str(msisdn)

            cursor.execute(f"INSERT INTO SDP.VPN_USERS (USER_NAME, PASSWORD, CUSTOMER_ID, CONFIG_ID, PROFILE_ID) "
                           f"VALUES ('{msisdn}', '{password}', {customer_id}, {config_id}, {profile_id})")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{msisdn}' AND CONFIG_ID={config_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class Contexts:
        @staticmethod
        def all(oracle, connection, cursor, context_id, context, vrf_count, is_full):
            """INSERT INTO SDP.VPN_CONTEXTS (CONTEXT_ID, CONTEXT, VRF_COUNT, IS_FULL)
            VALUES (1, 'Gi-3', 245, 0)

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context_id: 1
            :param context: 10000
            :param vrf_count: '10000_test'
            :param is_full: 10000
            :type context_id: int
            :type context: str
            :type vrf_count: int
            :type is_full: int

            Returns:
            :return: [{Select before delete}]
            :rtype: list"""
            cursor.execute(f"INSERT INTO SDP.VPN_CONTEXTS (CONTEXT_ID, CONTEXT, VRF_COUNT, IS_FULL) "
                           f"VALUES ({context_id}, '{context}', {vrf_count}, {is_full})")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            result = oracle.make_dictionary_results(cursor)
            return result

    class VRFs:
        @staticmethod
        def all(oracle, connection, cursor, context_id, rt_vrf, vrf_name, rd, rt):
            """INSERT INTO SDP.VPN_VRFS (CONTEXT_ID, RT_VRF, VRF_NAME, RD, RT)
            VALUES (1, 1, '10000_test', 10000, '10000, 10001')

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context_id: 1
            :param rt_vrf: 10000
            :param vrf_name: '10000_test'
            :param rd: 10000
            :param rt: '10000, 10001'
            :type context_id: int
            :type rt_vrf: int
            :type vrf_name: str
            :type rd: int
            :type rt: str

            Returns:
            :return: [{Select before delete}]
            :rtype: list"""
            cursor.execute(f"INSERT INTO SDP.VPN_VRFS (CONTEXT_ID, RT_VRF, VRF_NAME, RD, RT) "
                           f"VALUES ({context_id}, {rt_vrf}, '{vrf_name}', {rd}, '{rt}')")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RD={rd}")
            result = oracle.make_dictionary_results(cursor)
            return result


class Update:
    @staticmethod
    def update_by_query(cursor, query=f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID=1"):
        """Input manually query
        SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID=1"""
        cursor.execute(query)
        return query

    class Customers:
        @staticmethod
        def all(oracle, connection, cursor, unp, name, address, url, contact_name, contact_info, customer_id):
            """UPDATE SDP.VPN_CUSTOMERS SET UNP=123456789,NAME='Test',ADDRESS='Washington',URL='www',
            CONTACT_NAME='John',CONTACT_INFO='375291788765',
            EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss'),
            WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param unp: 123456789
            :param name: 'Test'
            :param address: 'Washington'
            :param url: 'www'
            :param contact_name: 'John'
            :param contact_info: '375291788765'
            :param customer_id: 1
            :type unp: int
            :type name: str
            :type address: str
            :type url: str
            :type contact_name: str
            :type contact_info: str
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            expiration_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"UPDATE SDP.VPN_CUSTOMERS "
                           f"SET UNP={unp},"
                           f"NAME='{name}',"
                           f"ADDRESS='{address}',"
                           f"URL='{url}',"
                           f"CONTACT_NAME='{contact_name}',"
                           f"CONTACT_INFO='{contact_info}',"
                           f"EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss'),"
                           f"WHERE CID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def unp_cid_equals(oracle, connection, cursor, unp, customer_id):
            """UPDATE SDP.VPN_CUSTOMERS SET UNP=123456789,
            EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss')
            WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param unp: 123456789
            :param customer_id: 1
            :type unp: str
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            expiration_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"UPDATE SDP.VPN_CUSTOMERS "
                           f"SET UNP={unp},"
                           f"EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss') "
                           f"WHERE CID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def name_cid_equals(oracle, connection, cursor, name, customer_id):
            """UPDATE SDP.VPN_CUSTOMERS SET NAME='Test',
            EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss')
            WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param name: 'Test'
            :param customer_id: 1
            :type name: str
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            expiration_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"UPDATE SDP.VPN_CUSTOMERS "
                           f"SET NAME='{name}',"
                           f"EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss') "
                           f"WHERE CID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def address_cid_equals(oracle, connection, cursor, address, customer_id):
            """UPDATE SDP.VPN_CUSTOMERS SET ADDRESS='Washington',
            EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss')
            WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param address: 'Washington'
            :param customer_id: 1
            :type address: str
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            expiration_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"UPDATE SDP.VPN_CUSTOMERS "
                           f"SET ADDRESS='{address}',"
                           f"EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss') "
                           f"WHERE CID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def url_cid_equals(oracle, connection, cursor, url, customer_id):
            """UPDATE SDP.VPN_CUSTOMERS SET URL='{url}',
            EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss')
            WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param url: 'www'
            :param customer_id: 1
            :type url: str
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            expiration_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"UPDATE SDP.VPN_CUSTOMERS "
                           f"SET URL='{url}',"
                           f"EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss') "
                           f"WHERE CID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def contact_name_cid_equals(oracle, connection, cursor, contact_name, customer_id):
            """UPDATE SDP.VPN_CUSTOMERS SET CONTACT_NAME='John W.V.',
            EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss')
            WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param contact_name: 'John W.V.'
            :param customer_id: 1
            :type contact_name: str
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            expiration_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"UPDATE SDP.VPN_CUSTOMERS "
                           f"SET CONTACT_NAME='{contact_name}',"
                           f"EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss') "
                           f"WHERE CID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def contact_info_cid_equals(oracle, connection, cursor, contact_info, customer_id):
            """UPDATE SDP.VPN_CUSTOMERS SET CONTACT_INFO='Full name company',
            EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss') "
            WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param contact_info: 'Full name company'
            :param customer_id: 1
            :type contact_info: str
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            expiration_date = str(datetime.now().isoformat(' ', 'seconds'))
            cursor.execute(f"UPDATE SDP.VPN_CUSTOMERS "
                           f"SET CONTACT_INFO='{contact_info}',"
                           f"EXPIRATION_DATE=to_date('{expiration_date}', 'yyyy-mm-dd hh24:mi:ss') "
                           f"WHERE CID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Profiles:
        @staticmethod
        def all(oracle, connection, cursor, profile_id, customer_id, profile_name, profile_type, config_id):
            """UPDATE SDP.VPN_PROFILES SET CUSTOMER_ID=1,PROFILE_NAME='Test',PROFILE_TYPE='static',CONFIG_ID=1
            WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param customer_id: 1
            :param profile_name: 'Test'
            :param profile_type: 'static'
            :param config_id: 1
            :type profile_id: int
            :type customer_id: int
            :type profile_name: str
            :type profile_type: str
            :type config_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_PROFILES "
                           f"SET CUSTOMER_ID={customer_id},"
                           f"PROFILE_NAME='{profile_name}',"
                           f"PROFILE_TYPE='{profile_type}',"
                           f"CONFIG_ID={config_id} "
                           f"WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def customer_id_pid_equals(oracle, connection, cursor, profile_id, customer_id):
            """UPDATE SDP.VPN_PROFILES SET CUSTOMER_ID=1 WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param customer_id: 1
            :type profile_id: int
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_PROFILES SET CUSTOMER_ID={customer_id} WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def profile_name_pid_equals(oracle, connection, cursor, profile_id, profile_name):
            """UPDATE SDP.VPN_PROFILES SET PROFILE_NAME='Test' WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param profile_name: 'Test'
            :type profile_id: int
            :type profile_name: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_PROFILES SET PROFILE_NAME='{profile_name}' WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def profile_type_pid_equals(oracle, connection, cursor, profile_id, profile_type):
            """UPDATE SDP.VPN_PROFILES SET PROFILE_TYPE='static' WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param profile_type: 'static'
            :type profile_id: int
            :type profile_type: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_PROFILES SET PROFILE_TYPE='{profile_type}' WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def config_id_pid_equals(oracle, connection, cursor, profile_id, config_id):
            """UPDATE SDP.VPN_PROFILES SET CONFIG_ID=1 WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param config_id: 1
            :type profile_id: int
            :type config_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_PROFILES SET CONFIG_ID={config_id} WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Dictionary:
        @staticmethod
        def all(oracle, connection, cursor, profile_id, customer_id, attribute_name, attribute_value):
            """UPDATE SDP.VPN_DICT SET CUSTOMER_ID=1, ATTRIBUTE_NAME='',ATTRIBUTE_VALUE=''
            WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param customer_id: 1
            :param attribute_name: ''
            :param attribute_value: ''
            :type profile_id: int
            :type customer_id: int
            :type attribute_name: str
            :type attribute_value: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_DICT "
                           f"SET CUSTOMER_ID={customer_id},"
                           f"ATTRIBUTE_VALUE='{attribute_value}' "
                           f"WHERE PROFILE_ID={profile_id} AND ATTRIBUTE_NAME='{attribute_name}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def customer_id_pid_equals(oracle, connection, cursor, profile_id, customer_id):
            """UPDATE SDP.VPN_DICT SET CUSTOMER_ID=1 WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param customer_id: 1
            :type profile_id: int
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_DICT SET CUSTOMER_ID={customer_id} WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def name_and_value_pid_equals(oracle, connection, cursor, profile_id, attribute_name, attribute_value):
            """UPDATE SDP.VPN_DICT SET ATTRIBUTE_VALUE=''
            WHERE PROFILE_ID=1 and ATTRIBUTE_NAME=''

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param attribute_name: ''
            :param attribute_value: ''
            :type profile_id: int
            :type attribute_name: str
            :type attribute_value: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_DICT "
                           f"SET ATTRIBUTE_VALUE='{attribute_value}' "
                           f"WHERE PROFILE_ID={profile_id} and ATTRIBUTE_NAME='{attribute_name}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Attributes:
        @staticmethod
        def all(oracle, connection, cursor, att_id, value, profile_id, config_id):
            """UPDATE SDP.VPN_ATTRIBUTES SET VALUE='172.24.202.111' WHERE CONFIG_ID=1 AND ATT_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param att_id: 1
            :param value: '172.24.202.111'
            :param profile_id: 1
            :param config_id: 1
            :type att_id: str
            :type value: int
            :type profile_id: int
            :type config_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_ATTRIBUTES SET VALUE='{value}' "
                           f"WHERE CONFIG_ID={config_id} AND ATT_ID={att_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Users:
        @staticmethod
        def all(oracle, connection, cursor, password, customer_id, config_id, profile_id, username):
            """UPDATE SDP.VPN_USERS SET PASSWORD='12345qwerty',CUSTOMER_ID=1,CONFIG_ID=1,PROFILE_ID=1
            WHERE USER_NAME='375291234567'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param password: '12345qwerty'
            :param customer_id: 1
            :param config_id: 1
            :param profile_id: 1
            :param username: '375291234567'
            :type password: str
            :type customer_id: int
            :type config_id: int
            :type profile_id: int
            :type username: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_USERS "
                           f"SET PASSWORD='{password}',"
                           f"CUSTOMER_ID={customer_id},"
                           f"CONFIG_ID={config_id},"
                           f"PROFILE_ID={profile_id} "
                           f"WHERE USER_NAME='{username}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def password_username_equals(oracle, connection, cursor, password, username):
            """UPDATE SDP.VPN_USERS SET PASSWORD='12345qwerty' WHERE USER_NAME='375291234567'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param password: '12345qwerty'
            :param username: '375291234567'
            :type password: str
            :type username: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_USERS SET PASSWORD='{password}' WHERE USER_NAME='{username}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def customer_id_username_equals(oracle, connection, cursor, customer_id, username):
            """UPDATE SDP.VPN_USERS SET CUSTOMER_ID=1 WHERE USER_NAME='375291234567'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param customer_id: 1
            :param username: '375291234567'
            :type customer_id: int
            :type username: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_USERS SET CUSTOMER_ID={customer_id} WHERE USER_NAME='{username}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def config_id_username_equals(oracle, connection, cursor, config_id, username):
            """UPDATE SDP.VPN_USERS SET CONFIG_ID=1 WHERE USER_NAME='375291234567'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param config_id: 1
            :param username: '375291234567'
            :type config_id: int
            :type username: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_USERS SET CONFIG_ID={config_id} WHERE USER_NAME='{username}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def profile_id_username_equals(oracle, connection, cursor, profile_id, username):
            """UPDATE SDP.VPN_USERS SET PROFILE_ID=1 WHERE USER_NAME='375291234567'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :param username: '375291234567'
            :type profile_id: int
            :type username: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_USERS SET PROFILE_ID={profile_id} WHERE USER_NAME='{username}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Contexts:
        @staticmethod
        def all(oracle, connection, cursor, context, vrf_count, is_full, context_id):
            """UPDATE SDP.VPN_CONTEXTS
            SET CONTEXT='Gi-3',VRF_COUNT=254,IS_FULL=0
            WHERE CONTEXT_ID=3

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context: 'Gi-3'
            :param vrf_count: 250
            :param is_full: 1
            :param context_id: 1
            :type context: str
            :type vrf_count: int
            :type is_full: int
            :type context_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_CONTEXTS SET CONTEXT='{context}',VRF_COUNT={vrf_count},IS_FULL={is_full} "
                           f"WHERE CONTEXT_ID={context_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def vrf_count_context_id_equals(oracle, connection, cursor, vrf_count, context_id):
            """UPDATE SDP.VPN_CONTEXTS SET VRF_COUNT=250 WHERE CONTEXT_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context_id: 1
            :param vrf_count: 250
            :type context_id: str
            :type vrf_count: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_CONTEXTS SET VRF_COUNT={vrf_count} WHERE CONTEXT_ID={context_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def vrf_count_context_equals(oracle, connection, cursor, vrf_count, context):
            """UPDATE SDP.VPN_CONTEXTS SET VRF_COUNT=250 WHERE CONTEXT='Gi-3'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context: 'Gi-3'
            :param vrf_count: 250
            :type context: str
            :type vrf_count: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_CONTEXTS SET VRF_COUNT={vrf_count} WHERE CONTEXT='{context}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def vrf_count_context_like(oracle, connection, cursor, vrf_count, context):
            """UPDATE SDP.VPN_CONTEXTS SET VRF_COUNT=250 WHERE CONTEXT LIKE '%Gi-3%'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context: 'Gi-3'
            :param vrf_count: 250
            :type context: str
            :type vrf_count: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT LIKE '%{context}%'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_CONTEXTS SET VRF_COUNT={vrf_count} WHERE CONTEXT LIKE '%{context}%'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT LIKE '%{context}%'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def is_full_context_id_equals(oracle, connection, cursor, is_full, context_id):
            """UPDATE SDP.VPN_CONTEXTS SET IS_FULL=1 WHERE CONTEXT_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param is_full: 1
            :param context_id: 1
            :type is_full: int
            :type context_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_CONTEXTS SET IS_FULL={is_full} WHERE CONTEXT_ID={context_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def is_full_context_equals(oracle, connection, cursor, is_full, context):
            """UPDATE SDP.VPN_CONTEXTS SET IS_FULL=1 WHERE CONTEXT='Gi-3'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param is_full: 1
            :param context: 'Gi-3'
            :type is_full: int
            :type context: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_CONTEXTS SET IS_FULL={is_full} WHERE CONTEXT='{context}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def is_full_context_like(oracle, connection, cursor, is_full, context):
            """UPDATE SDP.VPN_CONTEXTS SET IS_FULL=1 WHERE CONTEXT LIKE '%Gi-3%'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param is_full: 1
            :param context: 'Gi-3'
            :type is_full: int
            :type context: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT LIKE '%{context}%'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"UPDATE SDP.VPN_CONTEXTS SET IS_FULL={is_full} WHERE CONTEXT LIKE '%{context}%'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT LIKE '%{context}%'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class VRFs:
        pass


class Delete:
    @staticmethod
    def delete_by_query(connection, cursor, query=''):
        """Input manually query
        SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID=1"""
        cursor.execute(query)
        connection.commit()
        return query

    class Customers:
        @staticmethod
        def cid_equals(oracle, connection, cursor, cid):
            """DELETE FROM SDP.VPN_CUSTOMERS WHERE CID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param cid: 1
            :type cid: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={cid}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_CUSTOMERS WHERE CID={cid}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={cid}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def name_equals(oracle, connection, cursor, name):
            """DELETE FROM SDP.VPN_CUSTOMERS WHERE NAME='Test'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param name: 'Test'
            :type name: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE NAME='{name}'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_CUSTOMERS WHERE CID={old[0]['CID']}")
                connection.commit()
            except IndexError as e:
                print(f"Error: {e} : Row with NAME={name} is not exist")
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE CID={old[0]['CID']}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def name_like(oracle, connection, cursor, name):
            """DELETE FROM SDP.VPN_CUSTOMERS WHERE NAME LIKE '%Test%'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param name: 'Test'
            :type name: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE NAME LIKE '%{name}%'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_CUSTOMERS WHERE CID={old[0]['CID']}")
                connection.commit()
            except IndexError as e:
                print(f"Error: {e} : Row with NAME LIKE {name} is not exist")
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE NAME LIKE '%{name}%'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def unp_equals(oracle, connection, cursor, unp):
            """DELETE FROM SDP.VPN_CUSTOMERS WHERE UNP=123456789

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param unp: 123456789
            :type unp: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE UNP={unp}")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_CUSTOMERS WHERE CID={old[0]['CID']}")
                connection.commit()
            except IndexError as e:
                return {"error": f"Error: {e} : Row with UNP={unp} is not exist"}
            cursor.execute(f"SELECT * FROM SDP.VPN_CUSTOMERS WHERE UNP={unp}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Profiles:
        @staticmethod
        def cid_equals(oracle, connection, cursor, customer_id):
            """DELETE FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param customer_id: 1
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CUSTOMER_ID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def pid_equals(oracle, connection, cursor, profile_id):
            """DELETE FROM SDP.VPN_PROFILES WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :type profile_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def profile_name_equals(oracle, connection, cursor, profile_name):
            """DELETE FROM SDP.VPN_PROFILES WHERE PROFILE_NAME='Test'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_name: 'Test'
            :type profile_name: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_NAME='{profile_name}'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_PROFILES WHERE PROFILE_ID={old[0]['PROFILE_ID']}")
                connection.commit()
            except IndexError as e:
                return {"error": f"Error: {e} : Row with PROFILE_NAME LIKE {profile_name} is not exist"}
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={old[0]['PROFILE_ID']}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def profile_name_like(oracle, connection, cursor, profile_name):
            """DELETE FROM SDP.VPN_PROFILES WHERE PROFILE_NAME LIKE '%Test%'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_name: 'Test'
            :type profile_name: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_NAME LIKE '%{profile_name}%'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_PROFILES WHERE PROFILE_ID={old[0]['PROFILE_ID']}")
                connection.commit()
            except IndexError as e:
                return {"error": f"Error: {e} : Row with PROFILE_NAME LIKE '{profile_name}' is not exist"}
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE PROFILE_ID={old[0]['PROFILE_ID']}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def config_id_equals(oracle, connection, cursor, config_id):
            """DELETE FROM SDP.VPN_PROFILES WHERE CONFIG_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param config_id: 1
            :type config_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CONFIG_ID={config_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_PROFILES WHERE CONFIG_ID={config_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_PROFILES WHERE CONFIG_ID={config_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Dictionary:
        @staticmethod
        def cid_equals(oracle, connection, cursor, customer_id):
            """DELETE FROM SDP.VPN_DICT WHERE CUSTOMER_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param customer_id: 1
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_DICT WHERE CUSTOMER_ID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_DICT WHERE CUSTOMER_ID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_DICT WHERE CUSTOMER_ID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def pid_equals(oracle, connection, cursor, profile_id):
            """DELETE FROM SDP.VPN_DICT WHERE PROFILE_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :type profile_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_DICT WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_DICT WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_DICT WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Attributes:
        @staticmethod
        def config_id_equals(oracle, connection, cursor, config_id):
            """DELETE FROM SDP.VPN_ATTRIBUTES WHERE CONFIG_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param config_id: 1
            :type config_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE CONFIG_ID={config_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_ATTRIBUTES WHERE CONFIG_ID={config_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_ATTRIBUTES WHERE CONFIG_ID={config_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Users:
        @staticmethod
        def username_equals(oracle, connection, cursor, username):
            """DELETE FROM SDP.VPN_USERS WHERE USER_NAME='375291797391'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param username: 1
            :type username: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE USER_NAME='{username}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def customer_id_equals(oracle, connection, cursor, customer_id):
            """DELETE FROM SDP.VPN_USERS WHERE CUSTOMER_ID=1'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param customer_id: 1
            :type customer_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE CUSTOMER_ID={customer_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_USERS WHERE CUSTOMER_ID={customer_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE CUSTOMER_ID={customer_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def profile_id_equals(oracle, connection, cursor, profile_id):
            """DELETE FROM SDP.VPN_USERS WHERE PROFILE_ID=1'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param profile_id: 1
            :type profile_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PROFILE_ID={profile_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_USERS WHERE PROFILE_ID={profile_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PROFILE_ID={profile_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def config_id_equals(oracle, connection, cursor, config_id):
            """DELETE FROM SDP.VPN_USERS WHERE CONFIG_ID=1'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param config_id: 1
            :type config_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE CONFIG_ID={config_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_USERS WHERE CONFIG_ID={config_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE CONFIG_ID={config_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def password_equals(oracle, connection, cursor, password):
            """DELETE FROM SDP.VPN_USERS WHERE PASSWORD='qwerty12345'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param password: 'qwerty12345'
            :type password: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PASSWORD='{password}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_USERS WHERE PASSWORD='{password}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PASSWORD='{password}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def password_like(oracle, connection, cursor, password):
            """DELETE FROM SDP.VPN_USERS WHERE PASSWORD LIKE '%qwerty12345%'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param password: 'qwerty12345'
            :type password: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PASSWORD LIKE '%{password}%'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_USERS WHERE PASSWORD='{old[0]['PASSWORD']}'")
                connection.commit()
            except IndexError as e:
                return {"error": f"Error: {e} : Row with PASSWORD LIKE '{password}' is not exist"}
            cursor.execute(f"SELECT * FROM SDP.VPN_USERS WHERE PASSWORD LIKE '%{password}%'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class Contexts:
        @staticmethod
        def context_id_equals(oracle, connection, cursor, context_id):
            """DELETE FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID=1

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context_id: 1
            :type context_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT_ID={context_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def context_equals(oracle, connection, cursor, context):
            """DELETE FROM SDP.VPN_CONTEXTS WHERE CONTEXT='Gi-3'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context: 'Gi-3'
            :type context: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{context}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def context_like(oracle, connection, cursor, context):
            """DELETE FROM SDP.VPN_VRFS WHERE CONTEXT='Gi-3'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context:'Gi-3'
            :type context: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT LIKE '%{context}%'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{old[0]['CONTEXT']}'")
                connection.commit()
            except IndexError as e:
                return {"error": f"Error: {e} : Row with CONTEXT LIKE '{context}' is not exist"}
            cursor.execute(f"SELECT * FROM SDP.VPN_CONTEXTS WHERE CONTEXT='{old[0]['CONTEXT']}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

    class VRFs:
        @staticmethod
        def context_id_equals(oracle, connection, cursor, context_id):
            """DELETE FROM SDP.VPN_VRFS WHERE CONTEXT_ID=3

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param context_id: 3
            :type context_id: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE CONTEXT_ID={context_id}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_VRFS WHERE CONTEXT_ID={context_id}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE CONTEXT_ID={context_id}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def rt_vrf_equals(oracle, connection, cursor, rt_vrf):
            """DELETE FROM SDP.VPN_VRFS WHERE RT_VRF=10000'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param rt_vrf: 10000
            :type rt_vrf: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT_VRF={rt_vrf}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_VRFS WHERE RT_VRF={rt_vrf}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT_VRF={rt_vrf}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def vrf_name_equals(oracle, connection, cursor, vrf_name):
            """DELETE FROM SDP.VPN_VRFS WHERE VRF_NAME='10000_test'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param vrf_name: '10000_test'
            :type vrf_name: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME='{vrf_name}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_VRFS WHERE VRF_NAME='{vrf_name}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME='{vrf_name}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def vrf_name_like(oracle, connection, cursor, vrf_name):
            """DELETE FROM SDP.VPN_VRFS WHERE VRF_NAME LIKE '%10000_test%'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param vrf_name: '%10000_test%'
            :type vrf_name: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME LIKE '%{vrf_name}%'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_VRFS WHERE VRF_NAME='{old[0]['VRF_NAME']}'")
                connection.commit()
            except IndexError as e:
                return {"error": f"Error: {e} : Row with VRF_NAME LIKE {vrf_name} is not exist"}
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE VRF_NAME LIKE '%{vrf_name}%'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def rd_equals(oracle, connection, cursor, rd):
            """DELETE FROM SDP.VPN_VRFS WHERE RD=10000

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param rd: 10000
            :type rd: int

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RD={rd}")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_VRFS WHERE RD={rd}")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RD={rd}")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def rt_equals(oracle, connection, cursor, rt):
            """DELETE FROM SDP.VPN_VRFS WHERE RT='10000, 10001'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param rt: example - '10000, 10001'
            :type rt: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT='{rt}'")
            old = oracle.make_dictionary_results(cursor)
            cursor.execute(f"DELETE FROM SDP.VPN_VRFS WHERE RT='{rt}'")
            connection.commit()
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT='{rt}'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}

        @staticmethod
        def rt_like(oracle, connection, cursor, rt):
            """DELETE FROM SDP.VPN_VRFS WHERE RT='%10000%'

            Parameters:
            :param oracle: object oracle
            :param connection: object connection
            :param cursor: object cursor
            :param rt: example - '10000'
            :type rt: str

            Returns:
            :return: {"old": [Select before delete], "new": [Select after delete]} or {"error": "Error text"}
            :rtype: dict"""
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT LIKE '%{rt}%'")
            old = oracle.make_dictionary_results(cursor)
            try:
                cursor.execute(f"DELETE FROM SDP.VPN_VRFS WHERE RT='{old[0]['RT']}'")
                connection.commit()
            except IndexError as e:
                return {"error": f"Error: {e} : Row with RT LIKE {rt} is not exist"}
            cursor.execute(f"SELECT * FROM SDP.VPN_VRFS WHERE RT LIKE '%{rt}%'")
            new = oracle.make_dictionary_results(cursor)
            return {"old": old, "new": new}


# ora = OracleDB()
# con, cur = ora.connect()
# print(Select().VRFs().all(ora, cur))
# print(Insert().VRFs().all(ora, con, cur, context_id=1, rt_vrf=10000, vrf_name='10000_test', rd=10000, rt='10000, 10001'))
# print(Delete().VRFs().rt_vrf_equals(ora, con, cur, '10000'))
# ora.close(con, cur)
