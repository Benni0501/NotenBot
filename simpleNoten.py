import mysql.connector


class SimpleNoten:
    def __init__(self):
        print(f"noten constructor")
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="noten",
            password="benni0501"
        )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("USE noten;")

    def getNoten(self, personId):
        sql = "SELECT fach, IFNULL(note, 'NULL') FROM noten WHERE id=%s AND %s"
        personId = str(personId)
        val = (personId, True)
        self.mycursor.execute(sql, val)
        return self.mycursor.fetchall()

    def setNote(self, fach, note, personId):
        sql = "UPDATE noten SET note = %s WHERE fach = %s AND id = %s"
        val = (note, fach, personId)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def getID(self, personName):
        sql = "SELECT id FROM person WHERE name = %s AND %s"
        val = (personName, True)
        self.mycursor.execute(sql, val)
        personId = self.mycursor.fetchall()
        #print(personId)
        personId = personId[0]
        personId = personId[0]
        #print(personId)
        return personId
