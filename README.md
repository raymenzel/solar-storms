# solar-storms
A data pipeline to track solar and predict solar storms.

### How to get this code
Clone the repository by running:

```
$ git clone https://github.com/raymenzel/solar_storms.git
$ cd solar_storms
```

### How to install this code.
To install this code in a virtual environment, run:

```
$ python3 -m venv env
$ source env/bin/activate  # if in bash.
$ pip install --upgrade pip
$ pip install .
```

### How to run server.
Before starting the server for the first time, the database must be
initialized.  For now, the database just uses `sqlite3`.  The path
to the database controlled using an environment variable, which must
always be set before the server is run:

```
$ export SOLAR_STORMS_DATABASE="<path to sqlite file>"  # if in bash.
```

Once that environment variable is set, the database can be initialized by running:

```
$ python3 -m flask --app solar_storms init-db
```

Now, a development server can be started with flask by running:

```
$ python3 -m flask --app solar_storms run
```

This application downloads realtime solar wind data from the NOAA/DSCOVR
satellite every minute and stores it in its database.  The retention time
that the data stays in the database can be configured (see below).  A simple
REST API is set up to make this data accessible.  It can be accessed by
visiting the `/api/solar-wind` route. In the near future, I hope to add
a dashboard to the applications home page.

### How the data pipeline is designed.
