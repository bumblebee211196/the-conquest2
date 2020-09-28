import os


def make_db_connection(app):
    sqlalchemy_database_uri = 'mysql+pymysql://{username}:{password}@{hostname}/{databasename}'.format(
        username=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'),
        hostname='b81aignjnhxhsyt2kcnq-mysql.services.clever-cloud.com',
        databasename=os.environ.get('DB_NAME'),
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
