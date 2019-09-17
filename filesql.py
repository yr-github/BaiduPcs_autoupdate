import sqlite3

class OperateSQL():
    def __init__(self,path,logger):
        self.path = path
        self.logger = logger


    def getConn(self):
        try:
            self.conn = sqlite3.connect(self.path)#数据库地址
        except sqlite3.Error as err:
            self.logger.info(err)
        return
    #获取文件md5，如果该文件尚未存储md5值，则存入传入的md5
    def getFileMd5(self,file_,md5_):
        try:
            self.getConn()
            cursor = self.conn.cursor()
            serchsql = "SELECT md5 FROM filemd5 WHERE file = \'%s\'" % (file_)
            cursor.execute(serchsql)
            results = cursor.fetchall()
            if len(results) == 0:
                results = 0
            else:
                results = results[0][0]
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return results
        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()
    def updateMd5(self,file_,md5_):
        try:
            self.getConn()
            cursor = self.conn.cursor()
            serchsql = "SELECT md5 FROM filemd5 WHERE file = \'%s\'" % (file_)
            cursor.execute(serchsql)
            results = cursor.fetchall()
            if len(results) == 0:
                inssql = "INSERT INTO filemd5 (file,md5) VALUES('%s','%s')" % (file_, md5_)
                cursor.execute(inssql)
            else:
                updatesql = "UPDATE filemd5 SET md5 = \'%s\'  WHERE file = \'%s\'" % (md5_, file_)
                cursor.execute(updatesql)
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return 1
        except sqlite3.Error as err:
            self.logger.info(err)
            return 0
        finally:
            if self.conn:
                self.conn.close()