import datetime

from database import db

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    influencer = db.relationship('Influencer', backref='user', uselist=False)
    sponsor = db.relationship('Sponsor', backref='user', uselist=False)

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(128))
    niche = db.Column(db.String(128))
    reach = db.Column(db.Integer)
    is_flagged = db.Column(db.Boolean, default=False)

    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.user.username,
            'email': self.user.email,
            'category': self.category,
            'niche': self.niche,
            'reach': self.reach,
            'is_verified': self.is_verified,
            'is_flagged': self.is_flagged
        }


class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    company_name = db.Column(db.String(128))
    industry = db.Column(db.String(128))
    budget = db.Column(db.Float)
    is_flagged = db.Column(db.Boolean, default=False)

    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(128), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(64), nullable=False)
    goals = db.Column(db.Text)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'))
    guidelines = db.Column(db.Text)
    is_flagged = db.Column(db.Boolean, default=False)
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'budget': self.budget,
            'visibility': self.visibility,
            'goals': self.goals,
            'guidelines': self.guidelines,
            'is_flagged': self.is_flagged
        }

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'))
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float, nullable=False)
    negotiated_payment_amount = db.Column(db.Float, nullable=True)
    negotiated_by = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(64), nullable=False)
    madeby = db.Column(db.String(64), nullable=False)

