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
* Clone *this* repo:
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

ADD TO THISSSSSS

* To start the app locally, *cd* into the `backend` directory
    * Make sure you're in an Environmental Variable by running `source env/bin/activate` in the terminal
    * Next, `cd` into the `project` directory and run `python manage.py runserver` to initiate the backend server
* Go to the `frontend` folder and run `npm start` to initiate the ReactJS code
* If the user is not logged in, they are promtped to. User can also create a login.
* Once logged in, user is brought to their inbox containing any messages recieved
* User can click on the left-hand navigation to bring them to various pages
    * The Sent page displays all messages the user has sent
    * The Compose page allows the user to create and send messages
* Clicking on the message titles in Inbox and Sent allows the user to view the whole message
* Individual messages can be deleted


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
