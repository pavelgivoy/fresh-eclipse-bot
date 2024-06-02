from ..models.db_conn import DatabaseConnection


def close_all_sessions():
    session = DatabaseConnection().session
    session.close_all()


def commit_changes():
    with DatabaseConnection() as session:
        session.commit()
