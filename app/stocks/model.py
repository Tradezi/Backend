from app import db, bcrypt
from datetime import datetime

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    def get_created_on(self):
        return self.created_on.strftime("%c")
    
    def get_updated_on(self):
        return self.updated_on.strftime("%c")

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return

    def commit(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return

    @staticmethod
    def delete_all_rows():
        Stock.query.delete()

    # @staticmethod
    # def get_user_via_email(email):
    #     user = User.query.filter_by(email=email).first()
    #     return user

    def __repr__(self):
        return "id: {}, company-name: {}, symbol: {}".format(self.id, \
            self.company_name, self.symbol)