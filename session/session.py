import hashlib
import json
import random
import sys
import os
sys.path.append(os.path.abspath('C:\\Users\\BEROOZDG\\OneDrive\\Desktop\\مکتب\\project\\framework'))
from app.models import Session as SessionModel
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.migrathons import engine
from sqlalchemy import select


def generate_session_id():
    return hashlib.sha256(f'{random.random()}'.encode()).hexdigest()

def create_session(user_id):
    with Session(engine) as session:
        session_id= generate_session_id()
        session_value =json.dumps([{'user_id': user_id}])
        now=datetime.now()
        two_days=timedelta(days=2)
        session_model=SessionModel(
            session_key=session_id,
            session_value=session_value,
            expire_date=now+two_days
    )
        session.add(session_model)
        session.commit()
    return session_id

def get_session(session_id):
    with Session(engine) as session:
        query = select(SessionModel).where(
            SessionModel.session_key==session_id
        )
        session_model=session.scalar(query)
        if session_model is None:
            return None
        elif session_model.expire_date < datetime.now():
            return None
    return json.loads(session_model.session_value)
