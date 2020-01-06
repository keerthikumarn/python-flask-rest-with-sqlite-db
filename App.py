from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
import os.path
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'test.db')
app.config['JWT_SECRET_KEY'] = 'my-ulti-secret'
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'c3bdc75b9740a9'
app.config['MAIL_PASSWORD'] = 'ca06acf28f7b5c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#Initiating the config objects
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

#DB creation
@app.cli.command('db.create')
def db_create():
    db.create_all()
    print('Database created successfully !')


@app.cli.command('db.drop')
def db_drop():
    db.drop_all()
    print('Database dropped successfully !')


@app.cli.command('db.seed')
def db_seed():

    #Developers
    dev1 = Developers(first_name = 'John', last_name = 'Daniel', module = 'KNOWN', prog_lang = 'Java')
    dev2 = Developers(first_name='Gilly', last_name='Crisp', module='UKNOWN', prog_lang='Java')
    dev3 = Developers(first_name='Honey', last_name='Creeper', module='DEADLY', prog_lang='Java')
    db.session.add(dev1)
    db.session.add(dev2)
    db.session.add(dev3)

    #Users
    test_user = Users(first_name = 'test', last_name = 'user', email = 'user@test.com', password = 'pass')
    db.session.add(test_user)

    #commit the data to the tables in the DB
    db.session.commit()
    print("Database seeding completed successfully !")

@app.route('/')
def hello_world():
    return "Hello World !!"


@app.route('/my_rest_api')
def my_rest_api():
    return jsonify(greeting = "Welcome to my rest API world !! Wowww..just amazing")


@app.route('/page_not_found')
def page_not_found():
    return jsonify(message="Page/Resource not found"), 404


@app.route('/params')
def params():
    name = request.args.get('name')
    score = int(request.args.get('score'))
    if score > 50:
        return jsonify(message = "You are qualified for the main exam.. Congratss")
    else:
        return jsonify(message="You are NOT qualified for the main exam.. Dumboo")


@app.route('/url_params/<string:name>/<int:score>')
def url_params(name: str, score: int):
    if score > 50:
        return jsonify(message = "You are qualified for the main exam.. Congratss")
    else:
        return jsonify(message="You are NOT qualified for the main exam.. Dumboo")



#retreive all the developers details
@app.route('/developers', methods = ['GET'])
def get_all_developers():
    dev_list = Developers.query.all()
    result = developers_schema.dump(dev_list)
    return jsonify(data=result)


#retreive all the user details
@app.route('/users', methods = ['GET'])
def get_all_users():
    print("Fetching all the users...")
    users_list = Users.query.all()
    result = users_schema.dump(users_list)
    return jsonify(data=result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test_user = Users.query.filter_by(email=email).first()
    if test_user:
        return jsonify(message = 'The email id already exists in the database')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        new_user = Users(first_name=first_name, last_name=last_name,email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User created successfully !!'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    user = Users.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Successful!", access_token=access_token)
    else:
        return jsonify(message="You have entered an invalid email or password"), 401


@app.route('/retrieve_pwd/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = Users.query.filter_by(email=email).first()
    if user:
        msg = Message("your REST API password is " + user.password,
                      sender="no-reply@myrestapi.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="User password sent to " + email)
    else:
        return jsonify(message="The email id doesn't exist"), 401



@app.route(('/developer_details/<int:dev_id>'), methods=['GET'])
def get_developer_details(dev_id: int):
    developer = Developers.query.filter_by(dev_id=dev_id)
    if developer is not None:
        result = developers_schema.dump(developer)
        return jsonify(result)
    else:
        return jsonify(message='User does not exist'), 404


@app.route('/add_dev', methods=['POST'])
@jwt_required
def add_developer():
    first_name = request.form['first_name']
    developer = Developers.query.filter_by(first_name=first_name).first()
    if developer:
        return jsonify("There is already a developer by that name"), 409
    else:
        last_name = request.form['last_name']
        module = request.form['module']
        prog_lang = request.form['prog_lang']

        new_developer = Developers(first_name=first_name,
                            last_name=last_name,
                            module=module,
                            prog_lang=prog_lang)

        db.session.add(new_developer)
        db.session.commit()
        return jsonify(message="You added a new User successfully !"), 201


@app.route('/update_dev', methods=['PUT'])
@jwt_required
def update_developer_details():
    dev_id = int(request.form['dev_id'])
    developer = Developers.query.filter_by(dev_id=dev_id).first()
    if developer:
        developer.first_name = request.form['first_name']
        developer.last_name = request.form['last_name']
        developer.module = request.form['module']
        developer.prog_lang = request.form['prog_lang']
        db.session.commit()
        return jsonify(message="You updated the developer details"), 202
    else:
        return jsonify(message="The developer does not exist"), 404


@app.route('/delete_dev/<int:dev_id>', methods=['DELETE'])
#@jwt_required
def delete_developer(dev_id: int):
    developer = Developers.query.filter_by(dev_id=dev_id).first()
    if developer:
        db.session.delete(developer)
        db.session.commit()
        return jsonify(message="Developer deleted successfully!!"), 202
    else:
        return jsonify(message="The developer does not exist"), 404


'''
Defining the DB models for the app
'''

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
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


#JSON Schema for Users Model
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


# JSON Schema for Developers Model
class DevelopersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'module', 'prog_lang')


users_schema = UserSchema()
users_schema = UserSchema(many=True)

developers_schema = DevelopersSchema()
developers_schema = DevelopersSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)
