from models.user import Userauth
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db

class repositoryUser():
    def getAllUser(self)->Userauth:
        return Userauth.query.all()
    def getAllUserDict(self)->dict:
        return list(map(lambda x: x.to_dict(),self.getAllUser()))
    def initializeFirstUser(self):
        adminUser = Userauth.query.all()
        if (len(adminUser)==0):
            hashed_pw = generate_password_hash("admin", method='pbkdf2:sha256')
            new_user = Userauth(username="admin@admin.com", password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            print("first User Initialized")

APIrepouser = repositoryUser()