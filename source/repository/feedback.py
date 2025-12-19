from database.db import db 
from models.feedback import feedback

class feedbackRepository():

    @classmethod
    def get_all_feedback(cls):
        return feedback.query.all()

    @classmethod
    def insert_feedback(
        cls,
        age=None,
        sex=None,
        fbs=None,
        restecg=None,
        exang=None,
        oldpeak=None,
        cp=None,
        chol=None,
        slope=None,
        ca=None,
        target=None,
        thal=None,
        pred_target=None,
        trestbps=None,
        valid=False
    ):
        """
        Creates and saves a new feedback record. 
        All arguments default to None (NULL in SQL).
        """
        new_feedback = feedback(
            age=age,
            sex=sex,
            fbs=fbs,
            restecg=restecg,
            exang=exang,
            oldpeak=oldpeak,
            cp=cp,
            chol=chol,
            slope=slope,
            ca=ca,
            target=target,
            thal=thal,
            pred_target=pred_target,
            trestbps=trestbps,
            valid=valid
        )
        
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback
    
    @classmethod
    def insert_feedback_json(cls,data):
        """
        Takes a dictionary of data, creates a new feedback object,
        saves it to the database, and returns the created object.
        """
        new_feedback = feedback(
            age=data.get('age'),
            sex=data.get('sex'),
            fbs=data.get('fbs'),
            restecg=data.get('restecg'),
            exang=data.get('exang'),
            oldpeak=data.get('oldpeak'),
            cp=data.get('cp'),
            chol=data.get('chol'),
            slope=data.get('slope'),
            ca=data.get('ca'),
            target=data.get('target'),
            thal=data.get('thal'),
            pred_target=data.get('pred_target'),
            trestbps=data.get('trestbps'),
            valid=data.get('valid', False) # Default to False if not provided
        )
        
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback