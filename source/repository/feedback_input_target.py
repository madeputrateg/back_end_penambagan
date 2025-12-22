from models.feedback_input_target import feedback_input_target
from database.db import db

class repository_feedback_input_target():
    def __init__(self,db):
        self.db = db

    def get_feedback_target(self)->list[feedback_input_target]:
        return feedback_input_target.query.all()
    
    def insertFeedback_target(self,target,pred_target,model_id) -> feedback_input_target:
        feedback_input = feedback_input_target(
            model_id = model_id,
            target = target,
            pred_target = pred_target,
            valid= False
        )
        self.db.session.add(feedback_input)
        self.db.session.commit()
        
        return feedback_input
    def update_feedback_validation(cls,input_id):
        row = db.session.query(feedback_input_target).filter(feedback_input_target.id == input_id).first()
        if row:
            row.valid = True
            db.session.commit()

            
APIrepoFeedbackTarget = repository_feedback_input_target(db)