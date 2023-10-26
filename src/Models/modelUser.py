

class ModelUser():
    
    @classmethod
    def login(self,db,user):
        from .userg import User
        try:
            cursor = db.cursor()
            cursor.execute("SELECT id,username,mail,password FROM login WHERE username = '{}' ".format(user.username))
            row = cursor.fetchone()
            if row != None:
                
                user = User(row[0],row[1],row[2],User.check_password(row[3],user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)    