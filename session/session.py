import hashlib
import random
import json
from app.models import Session as SessionModel
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.migartions import engine
from app.models import User
from sqlalchemy import select

def generate_session_id():

    return hashlib.sha256(f'{random.random()}'.encode()).hexdigest()

def creat_session(user_id):

    session_id =  generate_session_id()
    session_value = json.dumps({'user_id': user_id})

    with Session(engine) as session:
        
        session_model = SessionModel(
            session_key=session_id,
            session_value=session_value,
            expire_date=datetime.now()+timedelta(days=2))
    
        session.add(session_model)
        session.commit()
    return session_id

def get_session(session_id):
    with Session(engine) as session:

        query = select(SessionModel).where(
            SessionModel.session_key == session_id)
        session_model = session.scalar(query)
        if session_model is None:
            return None
        elif session_model.expire_date < datetime.now():
            return None
    return session_model

def destroy_session(session_id):
    if session_id in Session:
        del Session[session_id]