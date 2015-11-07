#
# 2015-11-07 
#
# simple mysql wrapper which lets us connect to and execut queries against 
# our mysql database.
#
import MySQLdb
import MySQLdb.cursors
import os

class MySQLDBConn:
    __host = "tejava-db.cyxt7rugzh4d.us-west-1.rds.amazonaws.com"
    __database = "tejava_db"
    __user = os.getenv("DB_USER", None)
    __password = os.getenv("DB_SECRET", None)
    __port = 3306


    def __enter__(self):
        return self
    

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()
    
    
    def __init__(self):
        try:
            self.__conn = MySQLdb.connect(
                    user=self.__user,
                    passwd=self.__password,
                    host=self.__host,
                    db=self.__database,
                    port=self.__port,
                    cursorclass=MySQLdb.cursors.DictCursor)

        except MySQLdb.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                printi("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        except Exception as e:
            print("Uncaught Exception: %s" % str(e))
            raise(e)


    def __del__(self):
        if self.__conn: self.__conn.close()
        self.__conn = None
    

    def executeReadQueryHash(self, query, fillers=()):
        """returns the results of the read query as a list of dicts. each dict is 1 row"""
        if not self.__conn: return None
        rows = None

        try:
            cursor = self.__conn.cursor()
            cursor.execute(query, fillers)
            rows = cursor.fetchall()
        except Exception as e:
            print(str(e))
            raise(e)
        finally:
            cursor.close()
            return rows


    def executeWriteQuery(self, query, fillers=()):
        """returns the number of rows affected by a delete, insert, or update query"""
        if not self.__conn: return None
        count = 0

        try:
            cursor = self.__conn.cursor()
            cursor.execute(query, fillers)
            self.__conn.commit()
            count = cursor.rowcount
        except Exception as e:
            self.__conn.rollback()
            print(str(e))
            raise(e)
        finally:
            cursor.close()
            return count
