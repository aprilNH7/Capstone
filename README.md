Udacity Final Project "Capstone"

Udacity Fullstack Developer Nanodegree Capstone Project combines all of the
concepts, and the skills taught in the courses to build an API from start to
finish and host it.

General Specifications

Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies
and managing and assigning actors to those movies. You are an Executive
Producer within the company and are creating a system to simplify and
streamline your process.

Key Dependencies:

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices
framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM
we'll use handle the lightweight sqlite database. You'll primarily work in
app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension
we'll use to handle cross origin requests from our frontend server.

Models:

Movies with attributes title and release date
Actors with attributes name, age and gender

Endpoints:

GET /actor and /movie
DELETE /actor/ and /movie/
POST /actor and /movie and
PATCH /actor/ and /movie/

Roles:

Casting Assistant
Can view actors and movies

Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies

Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database

Tests:
One test for success behavior of each endpoint
One test for error behavior of each endpoint
At least two tests of RBAC for each role

Setup virtual environment(mac instructions)

To create a virtual environment, run the venv module as a script in the
Capstone directory:

python3 -m venv myenv

Activate the virtual environment.
source myenv/bin/activate

Install all dependencies

Use pip to install the required dependencies.

pip install -r requirements.txt

Run the server

Start the server using the FLASK development server:

export FLASK_APP=app.py
export FLASK_ENV=development
python3 app.py
Open browser

Navigate to project homepage http://127.0.0.1:5000/


Roles:

Executive Producer
Can preform ALL permissions
Permissions:
get:actor - lists all actors
get:movie - lists all movies
patch:actor - edit existing actor
patch:movie - edit existing movie
post:actor - create a new actor
post:movie - create a new movie
delete:actor - delete an existing actor
delete:movie - delete an existing movie

Casting Director
Can get a list of all actors & movies, can patch actors & movies,
can create & delete an actor.
Permissions:
get:actor - lists all actors
get:movie - lists all movies
patch:actor - edit existing actor
patch:movie - edit existing movie
post:actor - create a new movie
delete:actor - delete an existing actor


Casting Assistant
Can get a list of actors & movies.
Permissions:
get:actor
get:movie

Endpoints

GET '/actor'
GET '/movie'
PATCH '/actor/<int:id>'
PATCH '/movie/<int:id>'
POST '/actor'
POST '/movie'
DELETE '/actor/<int:id>'
DELETE '/movie/<int:id>'

GET '/actor'
- Endpoint fetches a list of all actors.
- Request Arguments: None
- Returns: Includes a success: "True" message along with a list
of all actors in JSON format.

{
  'success': True,
  'actor': actor
}

GET '/movie'

- Endpoint fetches a list of all movies.
- Request Arguments: None
- Returns: Includes a success: "True" message along with a list
of all movies in JSON format.

{
  'success': True,
  'movie': movie
}

POST '/actor'

Creates a new actor
-Roles based authentication
Request Arguments:
Body: JSON object containing the name, age, and gender.
{
        'name' : 'name',
        'age' : age,
        'gender' : 'gender'
}
Returns: The same JSON data, if there are no errors.
{
        'name' : 'Alicia Keys',
        'age' : 35,
        'gender' : 'Female'
}

POST '/movie'

Creates a new movie
-Roles based authentication
Request Arguments:
Body: JSON object containing the title and releasedate.
{
         'title': 'title',
         'releasedate': 'releasedate'
}
Returns: The same JSON data, if there are no errors.
{
         'title': 'March Madness',
         'releasedate': 'September 12, 2022'
}

PATCH '/actor/id'
Edits an existing actor
-Roles based authentication
Request Arguments:

1. name(String)
2. age(Integer)
3. gender(String)
Returns:
{
        'success': True,
        'updated': actor
}

PATCH '/movie/id'
Edits an existing movie
-Roles based authentication
Request Arguments:

1. title(String)
2. releasedate(String)
Returns:
{
        'success': True,
        'movie': movie
}

DELETE '/actor/id'
Deletes an existing actor from the database
-Roles based authentication
Request Arguments:

1. id(Integer)- of the actor to delete
Returns: The id of the actor deleted, and a success message will appear if
there are no errors.
{
        'success': True,
        'deleted': id
}

DELETE '/movie/id'
Deletes an existing movie from the database
-Roles based authentication
Request Arguments:

1. id(Integer)- of the movie to delete
Returns: The id of the movie deleted, and a success message will appear if
there are no errors.
{
        'success': True,
        'deleted': id
}

...
Status Codes

Agency API returns the following status codes in its API:

Status Code	Description
200	Success
400	bad request
404	resource not found
405 method not allowed
422	unprocessable
500 internal server error
For all status codes a JSON object is included with a "success": Boolean and
the correct data or error code and message.

{
  "error": 405,
  "message": "method not allowed",
  "success": false
}

Tests:

To run the tests.
python3 tests.py
