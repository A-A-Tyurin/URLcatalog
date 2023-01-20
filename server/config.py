import os


class Config:
     BASEDIR = os.path.abspath(os.path.dirname(__file__))
     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db.sqlite3')
     SQLALCHEMY_TRACK_MODIFICATIONS = False
     UPLOAD_DIR = os.path.join(BASEDIR, 'uploads')
     LOG_DIR = os.path.join(BASEDIR, 'logs')
     LOG_PATH = os.path.join(LOG_DIR, 'app.log')
     ALLOWED_EXTENSIONS = ['csv']
     ROWS_PER_PAGE = 10

     @property
     def DEBUG(self):
          return os.getenv('DEBUG', False)

     @property
     def SECRET_KEY(self):
          return os.getenv('SECRET_KEY')
