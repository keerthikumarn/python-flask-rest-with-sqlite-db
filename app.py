from start import *
from db import *


@app.route('/')
def hello_world():
    return "Hello World !!"


@app.route('/my_rest_api')
def my_rest_api():
    return jsonify(
        greeting="Welcome to my rest API world !! Wowww..just amazing")


@app.route('/page_not_found')
def page_not_found():
    return jsonify(message="Page/Resource not found"), 404


@app.route('/params')
def params():
    name = request.args.get('name')
    score = int(request.args.get('score'))
    if score > 50:
        return jsonify(
            message="You are qualified for the main exam.. Congratss")
    else:
        return jsonify(
            message="You are NOT qualified for the main exam.. Dumboo")


@app.route('/url_params/<string:name>/<int:score>')
def url_params(name: str, score: int):
    if score > 50:
        return jsonify(
            message="You are qualified for the main exam.. Congratss")
    else:
        return jsonify(
            message="You are NOT qualified for the main exam.. Dumboo")


#retreive all the developers details
@app.route('/developers', methods=['GET'])
def get_all_developers():
    dev_list = Developers.query.all()
    result = developers_schema.dump(dev_list)
    return jsonify(data=result)


#retreive all the user details
@app.route('/users', methods=['GET'])
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
        return jsonify(message='The email id already exists in the database')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        new_user = Users(first_name=first_name,
                         last_name=last_name,
                         email=email,
                         password=password)
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
        return jsonify(
            message="You have entered an invalid email or password"), 401


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


if __name__ == '__main__':
    app.run(debug=True)
