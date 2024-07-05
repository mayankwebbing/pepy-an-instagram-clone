# PEPY - An Instagram Clone Web Application Using Django

This python web application focuses on creating basic functionalities provided by the `Instagram` listed below. 

To Do's:
- [x] Account Register, Login & Logout
- [ ] Profile Edit
- [ ] Private & Public Profile
- [x] Post
- [x] Comment & Reply
- [ ] Like
- [ ] Mutual Profile Suggestions
- [ ] Feed
- [ ] Explore
- [ ] Search
- [ ] Messaging

This project is meant for learning purpose and is open for your valuable suggestions & code reviews.


## Install Dependencies
To start this application it is suggested to create a virtual python environment, which will seperate all the dependencies from the python global interpreter.

```bash
python -m venv env
```

To activate the virtual environment which we created in Windows, run the following command.

```bash
.\env\Scripts\activate
```

Once activated you may see the enviroment name appearing on the terminal prompt, run the following command to upgrade the pip (python package manager).

```bash
python.exe -m pip install --upgrade pip
```

All the dependencies required for this project are listed in the `requirements.txt` file, to install all of them you need to run the below command in terminal.

```bash
pip install -r requirements.txt
```

If in future you wish to install any new dependencies, don't forget to update `requirements.txt` file by running below command.

```bash
pip freeze > requirements.txt
```

Voila! all of your dependencies are now installed, and now we can move forward with the database setup.

## Database Setup

Download PostgreSQL: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

Create a new user (recommended) and assign owner's permission to a new empty database.

You will find a `.my_pgpass` file in the root directory, which stores the sample configuration for your database setup. In this project I've used `PostgreSQL` hence you will find the configuration similar to it, you can change it to any of your database engine by updating the `DATABASES` variable in the `settings.py` file under `pepy` directory, which will also serve as the django project directory for this Instagram Clone application. Kindly refer to comments in case of any issue is faced.

Once done with the database configuration, you need to finally rename the sample db configuration file to `.pepy_pgpass` in the same directory. Now we can move forward for creating the database tables onto our database for our application.

Since we're using `Django` for this project, it is so much easy for us to migrate all the models to our database. `makemigrations <appname:optional>` command will create migration folder in the app directory which represents the table schema written as python code, to implement this changes we will be required to run `migrate <appname:optional>` command which then will reflect all the changes to our database.

#### Database Migration command
```bash
python manage.py makemigrations accounts
python manage.py migrate accounts

python manage.py makemigrations feed
python manage.py migrate feed

python manage.py makemigrations
python manage.py migrate
```

## SuperUser Setup

Now we are ready with the database setup. if you wish to watch the models on the django admin, you will be required to create a superuser (admin). Run the following command and fill the details when prompted.

```bash
python manage.py createsuperuser
```

Remeber the username and password as it will be required to login at the admin panel, to start the django server run following command.

```bash
python manage.py runserver
```

Once all the system checks are performed and no error is raised, you can see the success prompt on your terminal which means you're server is actively running and is ready to serve the web requests.

To visit our web application, navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

To visit the admin interface, navigate to [http://127.0.0.1:8000/securelogin/login/](http://127.0.0.1:8000/securelogin/login/).

The point which has to be noted here is, the default admin url of django is `admin` but for this project and due to security compliance I've customized it to `securelogin`.

## Extras

When you deploy a Django project to a production server, the server needs a single directory from which to serve these static files efficiently. To do so, run the following command.

```bash
python manage.py collectstatic
```

To write and execute SQL queries directly to inspect or manipulate data in the database. We can run following command as this can be useful for debugging, data analysis, or performing one-off operations.

It starts a database-specific interactive shell, like psql for PostgreSQL or mysql for MySQL, using the connection settings defined in your Django project's settings.py file.

```bash
python manage.py dbshell
```

To start an interactive Python shell within the context of Django project. Which means you have direct access to your project's models, functions, and settings, making it a powerful tool for a variety of tasks like `Testing and Debugging`, `Database Manipulation` and `Running Scripts`.

```bash
python manage.py shell
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the existing style and include appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
