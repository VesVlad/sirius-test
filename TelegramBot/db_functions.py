from sqlalchemy.orm import Session
from app import engine
from schema import Users, Context

def add_user(user_id):
    with Session(engine) as session:
        user = session.query(Users).filter_by(name=user_id).one_or_none()
        if user is None:
            session.add(Users(name=user_id))
            session.commit()
        else:
            session.close()

def add_context(user, answer: str):
    with Session(engine) as session:
        user = session.query(Users).filter_by(name=user).one_or_none()
        if user:
            session.add(Context(context_id=user.id, context=answer))
            session.commit()
        else:
            session.close()

def get_context(user):
    with Session(engine) as session:
        user = session.query(Users).filter_by(name=user).one_or_none()
        if user:
            contexts = session.query(Context).filter(Context.context_id==user.id).all()
            if len(contexts) != 0:
                return contexts[-1].context
        return ""

def remove_context(user):
    with Session(engine) as session:
        user = session.query(Users).filter_by(name=user).one_or_none()
        print(user.id)
        if user:
            objs = session.query(Context).filter(Context.context_id==user.id).delete()
            session.commit()
        else:
            session.close()