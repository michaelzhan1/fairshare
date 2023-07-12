class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expensetrack.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'production'