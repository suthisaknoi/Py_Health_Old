import ping3

def ping_ip(ip):
    try:
        response_time = ping3.ping(ip)
        if response_time is None or response_time == False:
            print(f"Request timed out for {ip}")
            return False
        else:
            print(f"Ping to {ip} successful, response time: {response_time} seconds")
            return True
    except ping3.errors.PingError as e:
        print(f"Failed to ping {ip}: {e}")
        return False

# Example usage
# ip_address = "127.0.0.1"  # Google's public DNS server 61.19.112.123
# x = ping_ip(ip_address)
# if x == True:
#     print("successful")
# else:
#     print("NO successful")




import mysql.connector
from mysql.connector import Error

def connect_to_mysql(host, user, password, database,):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            sentmessage = 'Connection to MySQL database was successful'
            print("Connection to MySQL database was successful")
            connection.close()
            return True,sentmessage
        else:
            sentmessage = 'Failed to connect to the database'
            print("Failed to connect to the database")
            return False,sentmessage
    except connection.errors as e:
        print(f"Error: {e}")
        sentmessage = 'Failed to connect to the database'
        return False, sentmessage



# Example usage
host = "61.19.112.123"
user = "sa"
password = "sa"
database = "lotto"
myport = '3306'

result,sentmessage = connect_to_mysql(host, user, password, database,myport)
if result == True:
    print("Is Connect")
    print(sentmessage)
else:
    print("Is not Connect")
    print(sentmessage)