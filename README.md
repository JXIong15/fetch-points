# fetch-points
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Table of Contents
* [Description](#description)
* [Installations](#installations)
* [Functionality](#functionality)
* [Commands](#commands)
* [Technologies Used](#technologies-used)
* [Demo](#demo)
* [Future Ideas](#future-ideas)
* [Sources](#sources)


## Description
Users can add Payers and Transaction data for these payers. Points are spent based on Transaction Timestamp order, 
meaning the oldest points are used first. No payer's points will ever be negative.
* **GitHub:** https://github.com/JXIong15/fetch-points
<p><img src="https://i.imgur.com/oliYce0.png" width="100%"  stylealt="transactions ordered by oldest time stamp"/></p>
<p align="center">(Transactions are in order of TIMESTAMP instead of the order received (ID)</p>


## Installations
* Clone *this* repo in *command line*: `git clone ` and one of the links below
  * **HTTPS:** https://github.com/JXIong15/fetch-points.git
  * **SSH:** git@github.com:JXIong15/fetch-points.git
* `cd` into the project and install in your command line:
  * *python*: https://www.python.org/downloads/
  * *pip*: should automatically be installed with python above
  * *pipenv*: https://pipenv.pypa.io/en/latest/install/
    * run `pipenv install` to download provided packages to pipfile and project
    * run `pipenv shell` to enter the virtual environment


## Functionality
* For the purpose of this project, the environmental variables are given in `.env.EXAMPLE`. 
Delete the **.EXAMPLE** part to use the **.env** file
* It is recommended that you create your own superuser to access the Django Admin: `python manage.py createsuperuser`
* To start the app locally, run `python manage.py runserver` and go to `http://localhost:8000/admin`
  * there is currently no Frontend, so you will just see the Django Admin panel with its built-in forms
* Using **Postman** (or any similar application):
  * GET *http://localhost:8000/balance/* : returns a list of the current payer balances
  * GET *http://localhost:8000/payer/* : returns a list of the current payers
  * GET *http://localhost:8000/transaction/* : returns a list of the transactions from oldest timestamp
  * POST *http://localhost:8000/payer/* : data = `{'name'='NAME'}` will return the new payer's information
  * POST *http://localhost:8000/transaction/* : data = `{'name'='NAME', 'points'=int, timestamp=time}` will add the 
new points to the specified payer
  * POST *http://localhost:8000/spend/* : data = `{'points'=int}` will return a receipt of which payer(s) spent points 
and how many points each payer spent
    * points are spent in order of oldest transaction timestamp
  * DELETE *http://localhost:8000/payer/{payer_id}* : will delete the payer and all associated transactions to them


## Commands
* In the *virtual environment*, run:
  * Server: `python manage.py runserver`
  * Tests: `python manage.py test`
  * Webclient Requests: `python points/client.py`


## Technologies Used
* **Django** and **Django REST Framework**
* **Postman** to test API routes: https://www.postman.com/downloads/
* **environ** for secret keys
* **requests** for Python web client


## Results
* **Webclient Results**:
<p><img src="https://i.imgur.com/ht6eSnv.png" width="100%" height="100%" stylealt="webclient results"/></p>

* **Test Results**:
<p><img src="https://i.imgur.com/72YEB2F.png" width="100%" height="100%" stylealt="tests results"/></p>


## Future Ideas
* In *tests*, get `object.create()` to work so that the code efficiently runs
  * right now it makes API calls to `post` new objects
* Figure out how to connect Transaction and Payer models by Payer name rather than foreign key


## Sources
* Django Docs: https://docs.djangoproject.com/en/4.0/
* Python HTTP Requests: https://docs.python-requests.org/en/latest/


## License
Licensed under the [MIT License](LICENSE).

<p align="center">© 2021 Jou Xiong</p>
