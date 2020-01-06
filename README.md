# python-flask-rest-with-sqlite-db

### What is Flask framework?

  - Microframework for python based applications
  - Used to build fast performing APIs
  - Can be easily integrated with an existing python project
  - Used to receive HTTP requests
  - Used in routing HTTP requests to the controller
  - Dispatching the controller
  - Returning the HTTP response
	
### More features in Flask:

  - Supports plug n play model
  - Add extensions as needed from flask extensions library
  - Pick whichever required extensions
  - Good support for custom implementations
  
### When to use a full stack web framework?

  - When building a huge and complex web application
  - When certain things are required out of the box in developing a web application
  
### Benefits of Flask framework

  - Helps in development and release of fast performing APIs
  - Consumes very little code
  
### Flask is excellent for:

  - Prototyping a web project (using python) before the actual development
  - Can be used as sandbox for development
  - Can be used to test solutions for different libraries and modules
  
### Steps to setup this application
  * git clone https://github.com/keerthikumarn/Python-Flask-Demo.git
  * Navigate to the root folder of the project
  * run the command : python App.py
  
### REST APIs exposed in the application
  * https://localhost:5000/login
  * https://localhost:5000/my_rest_api
  * https://localhost:5000/page_not_found
  * https://localhost:5000/params
  * https://localhost:5000/developers
  * https://localhost:5000/users
  * https://localhost:5000/register
  * https://localhost:5000/developer_details/<int:dev_id>
  * https://localhost:5000/add_dev
  * https://localhost:5000/update_dev
  * https://localhost:5000/delete_dev/<int:dev_id>
  * https://localhost:5000/url_params/<string:name>/<int:score>
  * https://localhost:5000/retrieve_pwd/<string:email>
  
 ### How to configure and run this application
  * git clone https://github.com/keerthikumarn/python-flask-rest-with-sqlite-db.git
  *
   ```sh
	$ cd python-flask-rest-with-sqlite-db
	$ pip install -r requirements.txt
	$ SET FLASK_APP=App
	$ flask db.create
	$ flask db.seed
	$ python App.py
   ```
