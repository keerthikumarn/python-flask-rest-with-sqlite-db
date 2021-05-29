from start import *


'''
Defining the DB models for the app
'''


class Users(db.Model):
    '''
    class for handling users
    '''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


class Developers(db.Model):
    '''
    class for handling developers
    '''
    __tablename__ = 'developers'
    dev_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    module = Column(String)
    prog_lang = Column(String)

    def __init__(self, first_name, last_name, module, prog_lang):
        self.first_name = first_name
        self.last_name = last_name
        self.module = module
        self.prog_lang = prog_lang


# JSON Schema for Users Model
class UserSchema(ma.Schema):
    '''
    class for users schema
    '''
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


# JSON Schema for Developers Model
class DevelopersSchema(ma.Schema):
    '''
    class for developers schema
    '''
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'module', 'prog_lang')


users_schema = UserSchema(many=True)
developers_schema = DevelopersSchema(many=True)
