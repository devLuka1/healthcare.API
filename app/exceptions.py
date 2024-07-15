from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError

class IntegrityError(SQLAlchemyIntegrityError):
    pass
