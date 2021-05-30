import os
import os.path

# setting up database uri
db_name = 'test.db'
base_dir = os.path.abspath(os.path.dirname(__file__))
database_uri = 'sqlite:///' + os.path.join(base_dir, db_name)

# jwt secret key
jws_secret_key = 'my-ulti-secret'

# mail server
mail_server = 'smtp.mailtrap.io'
mail_port = 2525
mail_username = 'c3bdc75b9740a9'
mail_password = 'ca06acf28f7b5c'
use_tls = True
use_ssl = False


# constants
min_passing_marks = 50

# response codes
error_resource_not_found = 401
error_resource_already_exists = 409
success_response = 201

# messages
login_success = 'Login Successful!'
email_already_exists = 'The email id already exists in the database'
user_create_success = 'User created successfully !!'
invalid_email_pwd = 'You have entered an invalid email or password'
no_user_exists = 'User does not exist'
