import mysql.connector
mydp = mysql.connector.connect(host="us-cdbr-east-05.cleardb.net", user="b4d000ad198399", password="50f8de4c", database="heroku_bae5d1263304f6d",
                               auth_plugin='mysql_native_password')

if (mydp):
    print("connected")
    mycursor = mydp.cursor()
else:
    print("Notconnected")


def get_reviews(x):
    if (mydp):
        print("connected")
        mycursor = mydp.cursor()
        return ['connected', 'sql']
    else:
        print("Notconnected")
        return ['not connected', 'sql']