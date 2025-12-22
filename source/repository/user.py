from models.user import Userauth


class repositoryUser():
    def getAllUser(self)->Userauth:
        return Userauth.query.all()
    def getAllUserDict(self)->dict:
        return list(map(lambda x: x.to_dict(),self.getAllUser()))

APIrepouser = repositoryUser()