#from conString import connectionString
import pymysql
import pymysql.cursors

connectionString = dict(
    host = '',
    user = '',
    password = '',
    dbname = ''
)

class DataBase(object):

    def __init__(self):
        self.connection = pymysql.connect(
            host = connectionString['host'],
            user = connectionString['user'],
            password = connectionString['password'],
            db = connectionString['dbname'],
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )
        print('Соединение с базой данных открыто')
    

    def getLessons(self,group,day):
        with self.connection.cursor() as cursor:
            query = 'SELECT l.FIO_Lecturer, c.Time,c.room,c.Course ,c.Type\
                        FROM class c,lecturer l \
                            where c.ID_Lecturer = l.Id_Lectur and c.GroupName = %s \
                                and c.day = %s;'
            cursor.execute(query,(group,day))
            return cursor.fetchall()

    def getRoom(self,room):
        with self.connection.cursor() as cursor:
            query = 'Select GroupName,Time, day \
                            from class \
                                where room = %s \
                                    '
            cursor.execute(query,room)
            return cursor.fetchall()


    def getLecturer(self,name):
        with self.connection.cursor() as cursor:
            query = 'Select c.day,c.Time,c.room \
                            from lecturer l, class c \
                                where l.FIO_Lecturer = %s \
                                    and l.Id_Lectur = c.Id_Lecturer \
                                        Order by c.day'
            cursor.execute(query,name)
            return cursor.fetchall()

    
    
    def getGroups(self,name):
        with self.connection.cursor() as cursor:
            query = 'Select GroupName \
                            from group_ \
                                where GroupName = %s'
            cursor.execute(query,name)
            return cursor.fetchall()

    def saveNewUser(self,id):
        with self.connection.cursor() as cursor:
            query = 'Insert into \
                            user(Group_Name,chat_id,type,state) \
                                values ("none",%s,"Anon","Main")'
            cursor.execute(query,id)
            return cursor.fetchall()

    def updateDataUser(self,user):
        with self.connection.cursor() as cursor:
            query = 'Update user \
                            set Group_Name = %s,type = %s,state = %s \
                                where chat_id = %s'
            cursor.execute(query,(user.group,user.type,user.state,user.id))
            return cursor.fetchall()

    def getUsers(self):
        with self.connection.cursor() as cursor:
            query = 'Select * from user'
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        self.connection.commit()
        print('Соединение с базой данных закрыто')
        self.connection.close()
    