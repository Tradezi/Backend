from datetime import datetime

from app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String) # hashed
    email_verified = db.Column(db.Boolean, default=False)

    sign_in_count = db.Column(db.Integer, default=0)

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

    def increment_sign_in_count(self):
        num = self.sign_in_count + 1
        self.sign_in_count = num
        db.session.commit()

    def check_hash_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def generate_hash_password(password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    @staticmethod
    def username_exists(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return False
        return True

    @staticmethod
    def email_exists(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return False
        return True

    def __repr__(self):
        return 'id: {}, username: {}, email: {}, sign_in_count: {}, created_on: {}'.format(self.id, self.username, \
                self.email, self.sign_in_count, self.get_created_on())