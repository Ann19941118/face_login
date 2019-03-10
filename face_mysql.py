import mysql.connector
import datetime


class face_mysql:
    def __init__(self):
        pass

    # 设置数据库和密码
    def conn_mysql(self):
        # TODO
        db = mysql.connector.connect(user='root', password='000000', host='127.0.0.1', database='face')
        return db

    def insert_facejson(self, pic_name, pic_json, uid, ugroup):
        db = self.conn_mysql()
        cursor = db.cursor()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into face_json(json,pic_name,date,state,uid,ugroup) values('%s', '%s', '%s', '%d', '%s', '%s');" % (
            pic_json, pic_name, dt, 1, uid, ugroup)
        print("insert sql= %r" % sql)
        lastid = None
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            lastid = int(cursor.lastrowid)
            db.commit()
            print('Successfully committed.')
        except:
            # Rollback in case there is any error
            db.rollback()
            print('Failed commit.')
        db.close()
        return lastid

    def findall_facejson(self, ugroup):
        db = self.conn_mysql()
        cursor = db.cursor()

        sql = "select * from face_json where state=1 and ugroup= '%s';" % ugroup
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            print("Error:unable to fetch data")
        db.close()
