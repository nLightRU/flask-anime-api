from contextlib import contextmanager
from flask import Flask
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class Database:
    def __init__(self):
        self.session_factory = None
        self.engine = None
        self.Session = None

    def init_app(self, app: Flask):
        db_url = URL.create(
            drivername='postgresql+psycopg',
            username=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            host=app.config['DB_HOST'],
            port = app.config['DB_PORT'],
            database=app.config['DB_NAME']
        )

        self.engine = create_engine(url=db_url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

        # app.teardown_appcontext(self.close_session)

    def close_session(self):
        self.Session.remove()

    @contextmanager
    def session_scope(self):
        session = self.Session()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


db = Database()