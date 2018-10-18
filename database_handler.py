import psycopg2
from file_handler import FileHandler
import json


class DatabaseHandler:
    def __init__(self):
        self.conn = psycopg2.connect(database="datamining", user="postgres", password="2251676", host='127.0.0.1')
        self.cur = self.conn.cursor()
        self.query = "insert into zoomit values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.parameters = []

    def executor(self):
        try:
            self.cur.execute(self.query,self.parameters)
            self.conn.commit()
        except psycopg2.IntegrityError as e:
            file_handler = FileHandler("db_logs.txt")
            file_handler.write("query=" + self.query)
            file_handler.write("parameters=" + str(self.parameters))
            file_handler.write(str(e))
        except psycopg2.DataError as e:
            file_handler = FileHandler("db_logs.txt")
            file_handler.write("query=" + self.query)
            file_handler.write("parameters=" + str(self.parameters))
            file_handler.write(str(e))

    def close(self):
        self.cur.close()
        self.conn.close()

    def set_query(self,query):
        self.query = query

    def prepare_query(self,fields):
        self.parameters = fields
        # sub_query = ""
        # for field in fields:
        #     sub_query += '"' + field + '",'
        # self.parameters = (sub_query)

    def select_query(self,parameter):
        self.query = "select title, direct_link, duration from videos_result_search where id = %s"
        self.parameters = [ parameter]
        self.executor()
        row = self.cur.fetchone()
        val = [row[0],json.loads(row[1]), row[2]]
        return val



# string = json.dumps(lst)
# lst = json.loads(string)

# def share_user_photo(_person):
#   _photo = Photo()
#   _photo.insert(_person.getUserId())
#   _qurey = "insert into photo values('"+_photo.getUserId()+"', '"+_photo.getPhotoId()+"', '"+_photo.getWriting()+"', '"\
#            +_photo.getAccessLevel()+"', '"+_photo.getDate()+"');"
#   db = qurey_in_database(_qurey)
#   close_database(db)

# def get_following(_person):
#   _qurey="select * from follow where userid='"+_person.getUserId()+"';"
#   db = qurey_in_database(_qurey)
#   _index=0
#   _following=[]
#   for a in db['cursor'].fetchall():
#     _following.append(Follow(userid = a[0], followuserid = a[1], date = a[2]))
#     for l1 in a:
#       print(l1, end=' ');
#     print("")
#     _index+=1
#   close_database(db)
#   return _following;


