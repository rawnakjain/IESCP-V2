import csv
import os
import time
from datetime import datetime
from functools import wraps
from io import StringIO
from celery import Celery
from celery.schedules import crontab
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required, current_user
)
from flask_mail import Message
from flask_restful import Api, Resource
from flask_security import SQLAlchemyUserDatastore, roles_required
from werkzeug.security import generate_password_hash, check_password_hash
from config import LocalDevelopmentConfig
from mailing import init_mail
from models import (
    User, Role, Sponsor, Influencer, Campaign, AdRequest
)
from flask_caching import Cache
from models import db

# import workers

app, api, jwt = None, None, None
cache = Cache()


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, origins=['http://localhost:8080'], supports_credentials=True)
    jwt = JWTManager(app)
    db.init_app(app)
    cache.init_app(app)
    app.app_context().push()
    db.create_all()

    api = Api(app)
    return app, api, jwt


app, api, jwt = create_app()
datastore = SQLAlchemyUserDatastore(db, User, Role)

celery = Celery('Application')

# Update celery app configurations
celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],  # Ensure this is set correctly
    timezone=app.config["CELERY_TIMEZONE"],
    broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
)


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(identity):
    return identity


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


with app.app_context():
    db.create_all()  # Create all tables
    # Check and create roles if they do not exist
    if not datastore.find_role('admin'):
        datastore.create_role(name='admin', description='You are an admin')

    if not datastore.find_role('sponsor'):
        datastore.create_role(name='sponsor', description='You are a sponsor')

    if not datastore.find_role('influencer'):
        datastore.create_role(name='influencer', description='You are an influencer')

    # Check and create admin user if it does not exist
    if not datastore.find_user(username='admin'):
        hashed_password = generate_password_hash('admin123')
        datastore.create_user(
            username='admin',
            email='admin@spark.com',
            password=hashed_password,
            active=True,
            roles=['admin']
        )
    db.session.commit()



def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or role not in [r.name for r in user.roles]:
                return jsonify({"message": "Access forbidden: insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
@app.post('/register')
def register():
    user_data = request.get_json()
    user_role = user_data.get('role')

    # Validate user data
    if not user_data['username']:
        return {"message": "Username is required"}, 400

    if not user_data['email']:
        return {"message": "Email is required"}, 400

    if not user_data['password']:
        return {"message": "Password is required"}, 400

    # Check if username already exists
    if datastore.find_user(username=user_data['username']):
        return {"message": "Username already taken"}, 400

    # Check if email already exists
    if datastore.find_user(email=user_data['email']):
        return {"message": "Email already registered"}, 400

    user = {
        'username': user_data.get('username'),
        'email': user_data.get('email'),
        'password': generate_password_hash(user_data.get('password')), }

    if user_role == 'sponsor':
        user = datastore.create_user(**user, active=False, roles=['sponsor'])
        db.session.add(user)
        db.session.commit()
        sponsor = Sponsor(user_id=user.id, company_name=user_data.get('sponsor_company'),
                          industry=user_data.get('sponsor_industry'),
                          budget=user_data.get('sponsor_budget'))
        db.session.add(sponsor)

    elif user_role == 'influencer':
        user = datastore.create_user(**user, active=True, roles=['influencer'])
        db.session.add(user)
        db.session.commit()
        influencer = Influencer(user_id=user.id, category=user_data.get('influencer_category'),
                                niche=user_data.get('influencer_niche'), reach=user_data.get('influencer_reach'))
        db.session.add(influencer)

    else:
        return {"message": "Invalid role"}, 400

    db.session.commit()
    return {"message": "User created successfully"}, 201


@app.post('/login')
def login():
    user_data = request.get_json()
    # Validate user data
    if not user_data.get('username'):
        return {"message": "Username is required"}, 400
    if not user_data.get('password'):
        return {"message": "Password is required"}, 400

    user = datastore.find_user(username=user_data['username'])
    if not user or not check_password_hash(user.password, user_data['password']):
        return {"message": "Invalid username or password"}, 401

    if not user.active:
        return {"message": "User is not active, please contact the admin"}, 401

    token = create_access_token(identity=user.id)
    role = user.roles[0].name
    return {
        "user_id": user.id,
        "username": user.username,
        "role": role,
        "token": token,
        "active": user.active,
        "expires_in": app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
    }, 200


# Restful APIs Starts Here

# Profile API
class UserProfile(Resource):
    @jwt_required()
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, 404

        profile_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.roles[0].name,
            "active": user.active
        }

        if 'sponsor' in profile_data["role"]:
            sponsor = Sponsor.query.filter_by(user_id=user.id).first()
            if sponsor:
                profile_data.update({
                    "sponsor_company": sponsor.company_name,
                    "sponsor_industry": sponsor.industry,
                    "sponsor_budget": sponsor.budget
                })

        elif 'influencer' in profile_data["role"]:
            influencer = Influencer.query.filter_by(user_id=user.id).first()
            if influencer:
                profile_data.update({
                    "influencer_category": influencer.category,
                    "influencer_niche": influencer.niche,
                    "influencer_reach": influencer.reach
                })

        return jsonify(profile_data)

    def put(self, username):
        user_data = request.get_json()
        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, 404

        if user_data.get('password'):
            user.password = generate_password_hash(user_data['password'])

        # Update role-specific fields
        if 'sponsor' in [role.name for role in user.roles]:
            sponsor = Sponsor.query.filter_by(user_id=user.id).first()
            if sponsor:
                sponsor.company_name = user_data.get('sponsor_company', sponsor.company_name)
                sponsor.industry = user_data.get('sponsor_industry', sponsor.industry)
                sponsor.budget = user_data.get('sponsor_budget', sponsor.budget)

        elif 'influencer' in [role.name for role in user.roles]:
            influencer = Influencer.query.filter_by(user_id=user.id).first()
            if influencer:
                influencer.category = user_data.get('influencer_category', influencer.category)
                influencer.niche = user_data.get('influencer_niche', influencer.niche)
                influencer.reach = user_data.get('influencer_reach', influencer.reach)

        db.session.commit()
        return {"message": "User updated successfully"}, 200


api.add_resource(UserProfile, '/api/profile/<string:username>')


# Sponsor APIs
class AllInfluencersList(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)

        influencers = Influencer.query.all()
        influencers_list = [
            {
                'id': influencer.id,
                'username': influencer.user.username,
                'email': influencer.user.email,
                'category': influencer.category,
                'niche': influencer.niche,
                'reach': influencer.reach,
                'is_verified': influencer.is_verified,
            }
            for influencer in influencers
        ]
        return jsonify(influencers_list)


api.add_resource(AllInfluencersList, '/api/influencers-list')


class SponsorCampaignsList(Resource):
    @jwt_required()  # fetching list of campaigns created by sponsor
    @role_required('sponsor')
    def get(self):
        # Get the current user's sponsor ID
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)
        sponsor_id = user.sponsor.id

        # Fetch all campaigns created by the sponsor
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()

        # Convert campaigns to a list of dictionaries
        campaigns_list = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'category': campaign.category,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
                'guidelines': campaign.guidelines,
                'is_flagged': campaign.is_flagged
            }
            for campaign in campaigns
        ]

        return jsonify(campaigns_list)


api.add_resource(SponsorCampaignsList, '/api/sponsor/campaigns-list')


class SponsorCampaigns(Resource):
    @jwt_required()
    @role_required('sponsor')
    def get(self, campaign_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)
        sponsor_id = user.sponsor.id

        # Fetch the campaign details
        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor_id).first()

        if not campaign:
            return {"message": "Campaign not found or you do not have permission to view this campaign"}, 404

        campaign_details = {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'category': campaign.category,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'guidelines': campaign.guidelines,
            'is_flagged': campaign.is_flagged
        }

        return jsonify(campaign_details)

    @jwt_required()
    @role_required('sponsor')
    def post(self):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)
        sponsor_id = user.sponsor.id
        data = request.get_json()

        # Convert date strings to datetime objects
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

        new_campaign = Campaign(
            name=data['name'],
            description=data['description'],
            category=data['category'],
            start_date=start_date,
            end_date=end_date,
            budget=data['budget'],
            visibility=data['visibility'],
            goals=data['goals'],
            sponsor_id=sponsor_id,
            guidelines=data['guidelines'],
            is_flagged=data.get('is_flagged', False)
        )

        db.session.add(new_campaign)
        db.session.commit()

        return {"message": "Campaign created successfully"}, 201

    @jwt_required()
    @role_required('sponsor')
    def put(self, campaign_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)
        sponsor_id = user.sponsor.id
        data = request.get_json()

        # Fetch the campaign to be updated
        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor_id).first()

        if not campaign:
            return {"message": "Campaign not found or you do not have permission to update this campaign"}, 404

        # Update campaign details
        campaign.name = data.get('name', campaign.name)
        campaign.description = data.get('description', campaign.description)
        campaign.category = data.get('category', campaign.category)
        campaign.start_date = datetime.strptime(data['start_date'],
                                                '%Y-%m-%d') if 'start_date' in data else campaign.start_date
        campaign.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') if 'end_date' in data else campaign.end_date
        campaign.budget = data.get('budget', campaign.budget)
        campaign.visibility = data.get('visibility', campaign.visibility)
        campaign.goals = data.get('goals', campaign.goals)
        campaign.guidelines = data.get('guidelines', campaign.guidelines)
        campaign.is_flagged = data.get('is_flagged', campaign.is_flagged)

        db.session.commit()

        return {"message": "Campaign updated successfully"}, 200

    @jwt_required()
    @role_required('sponsor')
    def delete(self, campaign_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)
        sponsor_id = user.sponsor.id

        # Fetch the campaign to be deleted
        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor_id).first()

        if not campaign:
            return {"message": "Campaign not found or you do not have permission to delete this campaign"}, 404

        db.session.delete(campaign)
        db.session.commit()

        return {"message": "Campaign deleted successfully"}, 200


api.add_resource(SponsorCampaigns, '/api/campaign', '/api/campaign/<int:campaign_id>')


# Ad Request APIs
class AdRequestResource(Resource):
    @jwt_required()
    def get(self, ad_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        if 'sponsor' not in [role.name for role in user.roles]:
            return {"message": "User is not a sponsor"}, 403

        ad = AdRequest.query.get(ad_id)
        if not ad:
            return {"message": "Ad not found"}, 404

        ad_details = {
            'id': ad.id,
            'campaign_id': ad.campaign_id,
            'influencer_id': ad.influencer_id,
            'requirements': ad.requirements,
            'payment_amount': ad.payment_amount,
            'negotiated_payment_amount': ad.negotiated_payment_amount,
            'status': ad.status,
            'madeby': ad.madeby,
        }
        return jsonify(ad_details)

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)
        data = request.get_json()

        new_ad = AdRequest(
            campaign_id=data['campaign_id'],
            influencer_id=data['influencer_id'],
            requirements=data['requirements'],
            payment_amount=data['payment_amount'],
            status=data["status"],
            madeby=user.roles[0].name,
        )

        db.session.add(new_ad)
        db.session.commit()

        return {"message": "Ad created successfully"}, 201

    @jwt_required()
    def put(self, ad_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        if 'sponsor' not in [role.name for role in user.roles]:
            return {"message": "User is not a sponsor"}, 403

        data = request.get_json()
        ad = AdRequest.query.get(ad_id)

        if not ad:
            return {"message": "Ad not found"}, 404

        ad.campaign_id = data.get('campaign_id', ad.campaign_id)
        ad.influencer_id = data.get('influencer_id', ad.influencer_id)
        ad.requirements = data.get('requirements', ad.requirements)
        ad.payment_amount = data.get('payment_amount', ad.payment_amount)
        ad.negotiated_payment_amount = data.get('negotiated_payment_amount', ad.negotiated_payment_amount)
        ad.status = data.get('status', ad.status)
        ad.madeby = data.get('madeby', ad.madeby)

        db.session.commit()

        return {"message": "Ad updated successfully"}, 200

    @jwt_required()
    def delete(self, ad_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        if 'sponsor' not in [role.name for role in user.roles]:
            return {"message": "User is not a sponsor"}, 403

        ad = AdRequest.query.get(ad_id)
        if not ad:
            return {"message": "Ad not found"}, 404

        db.session.delete(ad)
        db.session.commit()

        return {"message": "Ad deleted successfully"}, 200


api.add_resource(AdRequestResource, '/api/ad', '/api/ad/<int:ad_id>')


# Return the list of ads for a campaign
class CampaignAds(Resource):
    @jwt_required()
    @role_required('sponsor')
    def get(self, campaign_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        if 'sponsor' not in [role.name for role in user.roles]:
            return {"message": "User is not a sponsor"}, 403

        ads = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        ads_list = [
            {
                'id': ad.id,
                'campaign_id': ad.campaign_id,
                'influencer_id': ad.influencer_id,
                'requirements': ad.requirements,
                'payment_amount': ad.payment_amount,
                'negotiated_payment_amount': ad.negotiated_payment_amount,
                'negotiated_by': ad.negotiated_by,
                'status': ad.status,
                'madeby': ad.madeby,
            }
            for ad in ads
        ]
        return jsonify(ads_list)


api.add_resource(CampaignAds, '/api/ads-list/<int:campaign_id>')


class UpdateAdStatusResource(Resource):
    @jwt_required()
    def post(self, ad_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ['approved', 'declined', 'completed', 'negotiation']:
            return {"message": "Invalid status"}, 400

        ad = AdRequest.query.get(ad_id)
        if not ad:
            return {"message": "Ad not found"}, 404

        ad.status = new_status

        db.session.commit()

        return {"message": "Ad status updated successfully", 'ad': {
            'id': ad.id,
            'campaign_id': ad.campaign_id,
            'influencer_id': ad.influencer_id,
            'requirements': ad.requirements,
            'payment_amount': ad.payment_amount,
            'negotiated_payment_amount': ad.negotiated_payment_amount,
            'status': ad.status,
            'madeby': ad.madeby,
        }}, 200

    @jwt_required()
    def put(self, ad_id):
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        data = request.get_json()
        ad = AdRequest.query.get(ad_id)

        ad.negotiated_payment_amount = data.get('negotiated_payment_amount')
        ad.negotiated_by = user.roles[0].name
        ad.status = 'negotiation'

        db.session.commit()
        return {
            "message": "Request Sent Successfully",
            'ad': {
                'id': ad.id,
                'campaign_id': ad.campaign_id,
                'influencer_id': ad.influencer_id,
                'requirements': ad.requirements,
                'payment_amount': ad.payment_amount,
                'negotiated_payment_amount': ad.negotiated_payment_amount,
                'status': ad.status,
                'madeby': ad.madeby,
            }
        }, 200


api.add_resource(UpdateAdStatusResource, '/api/ad/update-status/<int:ad_id>')


class SearchResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        role = data.get('role')
        option = data.get('option')
        search_query = data.get('searchQuery')

        if role == 'sponsor':
            if option == 'influencer_username':
                results = Influencer.query.join(User).filter(User.username.ilike(f'%{search_query}%')).all()
            elif option == 'reach':
                results = Influencer.query.filter(Influencer.reach.ilike(f'%{search_query}%')).all()
            elif option == 'category':
                results = Influencer.query.filter(Influencer.category.ilike(f'%{search_query}%')).all()
            elif option == 'niche':
                results = Influencer.query.filter(Influencer.niche.ilike(f'%{search_query}%')).all()
            else:
                return {"message": "Invalid search option for sponsor"}, 400

        elif role == 'influencer':
            if option == 'campaign_name':
                results = Campaign.query.filter(Campaign.name.ilike(f'%{search_query}%')).all()
            elif option == 'budget':
                results = Campaign.query.filter(Campaign.budget.ilike(f'%{search_query}%')).all()
            elif option == 'category':
                results = Campaign.query.filter(Campaign.category.ilike(f'%{search_query}%')).all()
            else:
                return {"message": "Invalid search option for influencer"}, 400

        else:
            return {"message": "Invalid role"}, 400

        results_list = [result.to_dict() for result in results]
        return jsonify(results_list)


api.add_resource(SearchResource, '/api/search')


# Influencer APIs

# Return the list of all campaigns
class AllCampaignsList(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self):
        campaigns = Campaign.query.all()
        campaigns_list = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'category': campaign.category,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
                'guidelines': campaign.guidelines,
                'is_flagged': campaign.is_flagged
            }
            for campaign in campaigns
        ]
        return jsonify(campaigns_list)


api.add_resource(AllCampaignsList, '/api/campaigns-list')


# Return the list of ads belongs to an influencer
class InfluencerAdRequests(Resource):
    @jwt_required()
    @role_required('influencer')
    def get(self, influencer_username):
        # current_user_id = get_jwt_identity()
        # user = db.session.get(User, current_user_id)

        influencer = User.query.filter_by(username=influencer_username).first()
        influencer_id = influencer.influencer.id
        if not influencer or not influencer.influencer:
            return {"message": "Influencer not found"}, 404

        ads = AdRequest.query.filter_by(influencer_id=influencer_id).all()
        ads_list = [
            {
                'id': ad.id,
                'campaign_id': ad.campaign_id,
                'influencer_id': ad.influencer_id,
                'requirements': ad.requirements,
                'payment_amount': ad.payment_amount,
                'negotiated_payment_amount': ad.negotiated_payment_amount,
                'negotiated_by': ad.negotiated_by,
                'status': ad.status,
                'madeby': ad.madeby,
            }
            for ad in ads
        ]
        return jsonify(ads_list)


api.add_resource(InfluencerAdRequests, '/api/influencer/ads-list/<string:influencer_username>')


class InfluencerCampaigns(Resource): # Return the list of campaigns that an influencer has applied for
    @jwt_required()
    @role_required('influencer')
    def get(self, influencer_username):
        influencer = User.query.filter_by(username=influencer_username).first()
        if not influencer or not influencer.influencer:
            return {"message": "Influencer not found"}, 404

        influencer_id = influencer.influencer.id
        ad_requests = AdRequest.query.filter_by(influencer_id=influencer_id).all()
        campaign_ids = {ad.campaign_id for ad in ad_requests}
        campaigns = Campaign.query.filter(Campaign.id.in_(campaign_ids)).all()

        campaigns_list = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'category': campaign.category,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
                'guidelines': campaign.guidelines,
                'is_flagged': campaign.is_flagged
            }
            for campaign in campaigns
        ]

        return jsonify(campaigns_list)


api.add_resource(InfluencerCampaigns, '/api/influencer/campaigns-list/<string:influencer_username>')


# Admin APIs

class AllSponsorsList(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        sponsors = Sponsor.query.all()
        sponsors_list = [
            {
                'id': sponsor.id,
                'username': sponsor.user.username,
                'email': sponsor.user.email,
                'company_name': sponsor.company_name,
                'industry': sponsor.industry,
                'budget': sponsor.budget,
                'is_flagged': sponsor.is_flagged,
                'active': sponsor.user.active
            }
            for sponsor in sponsors
        ]
        return jsonify(sponsors_list)


api.add_resource(AllSponsorsList, '/api/sponsors-list')


class FlagCampaignResource(Resource):
    @jwt_required()
    @role_required('admin')
    def post(self, campaign_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {"message": "Campaign not found"}, 404

        # Flag the campaign
        campaign.is_flagged = True
        db.session.commit()

        return {"message": "Campaign flagged successfully", "campaign": campaign.to_dict()}, 200


api.add_resource(FlagCampaignResource, '/api/campaign/flag/<int:campaign_id>')


class UnFlagCampaignResource(Resource):
    @jwt_required()
    @role_required('admin')
    def post(self, campaign_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        # Check if the user is an admin
        if 'admin' not in [role.name for role in user.roles]:
            return {"message": "User is not an admin"}, 403

        # Fetch the campaign to be flagged
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {"message": "Campaign not found"}, 404

        # Flag the campaign
        campaign.is_flagged = False
        db.session.commit()

        return {"message": "Campaign unflagged successfully", "campaign": campaign.to_dict()}, 200


api.add_resource(UnFlagCampaignResource, '/api/campaign/unflag/<int:campaign_id>')


class VerifyInfluencerResource(Resource):
    @jwt_required()
    @role_required('admin')
    def post(self, influencer_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        # Check if the user is an admin
        if 'admin' not in [role.name for role in user.roles]:
            return {"message": "User is not an admin"}, 403

        # Fetch the influencer to be verified
        influencer = Influencer.query.get(influencer_id)
        if not influencer:
            return {"message": "Influencer not found"}, 404

        # Verify the influencer
        influencer.is_verified = True
        db.session.commit()

        return {"message": "Influencer verified successfully", "influencer": influencer.to_dict()}, 200


api.add_resource(VerifyInfluencerResource, '/api/influencer/verify/<int:influencer_id>')


class ApproveSponsorResource(Resource):
    @jwt_required()
    @role_required('admin')
    def post(self, sponsor_id):
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return {"message": "Sponsor not found"}, 404

        user = User.query.get(sponsor.user_id)
        if not user:
            return {"message": "User not found"}, 404

        user.active = True
        db.session.commit()
        print('we are at the end')
        return {"message": "Sponsor approved successfully"}, 200


api.add_resource(ApproveSponsorResource, '/api/sponsor/approve/<int:sponsor_id>')


class UserbaseDataResource(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if 'admin' not in [role.name for role in user.roles]:
            return {"message": "User is not an admin"}, 403

        roles = Role.query.all()
        role_names = [role.name for role in roles]
        user_counts = [User.query.join(User.roles).filter(Role.name == role.name).count() for role in roles]

        return jsonify({"roles": role_names, "user_counts": user_counts})


api.add_resource(UserbaseDataResource, '/api/admin/userbase-data')


class CampaignDataByCategoryResource(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if 'admin' not in [role.name for role in user.roles]:
            return {"message": "User is not an admin"}, 403

        campaigns = db.session.query(
            Campaign.category, db.func.count(Campaign.id).label('campaign_count')
        ).group_by(Campaign.category).all()

        categories = [campaign.category for campaign in campaigns]
        campaign_counts = [campaign.campaign_count for campaign in campaigns]

        return jsonify({"categories": categories, "campaign_counts": campaign_counts})

api.add_resource(CampaignDataByCategoryResource, '/api/admin/campaign-data')

class AdRequestDataByStatusResource(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if 'admin' not in [role.name for role in user.roles]:
            return {"message": "User is not an admin"}, 403

        ad_requests = db.session.query(
            AdRequest.status, db.func.count(AdRequest.id).label('ad_count')
        ).group_by(AdRequest.status).all()

        statuses = [ad_request.status for ad_request in ad_requests]
        ad_counts = [ad_request.ad_count for ad_request in ad_requests]

        return jsonify({"statuses": statuses, "ad_counts": ad_counts})

api.add_resource(AdRequestDataByStatusResource, '/api/admin/ads-data')

# ----------- All the micro services or celery tasks will be added here ------------###


mail = init_mail()


@celery.task()
def daily_reminder():
    pending_requests = db.session.query(
        AdRequest.influencer_id, db.func.count(AdRequest.id).label('pending_count')
    ).filter(
        AdRequest.status == 'pending',
        AdRequest.madeby == 'sponsor'
    ).group_by(
        AdRequest.influencer_id
    ).all()

    # Collecting email addresses of influencers with pending requests
    recipients = []
    for influencer_id, pending_count in pending_requests:
        if pending_count > 0:
            influencer = Influencer.query.get(influencer_id)
            recipients.append((influencer.user.email, influencer.user.username, pending_count))

    if recipients:
        with mail.connect() as conn:
            subject = "IESCP V2 Reminder"
            for recipient, username, pending_count in recipients:
                message_content = "<h1 class='card-title text-success'>Daily Reminder: Visit SPARK App</h1>"
                message_content += f"<p class='card-text'>Hello, {username}&nbsp;! You have {pending_count} pending ad requests from sponsors.</p>"
                message_content += "<p class='card-text'>This is a friendly reminder to visit SPARK App and explore our latest offerings. We have exciting campaigns and ads waiting for you!</p>"
                message_content += "<p class='card-text'>Don't miss out on the amazing campaign options. Click the link below to start your SPARK experience:</p>"
                message_content += "<a href='http://localhost:8080/' class='btn btn-success'>Visit Spark App</a>"
                message_content += "<p class='card-text mt-3'>If you have any questions or need assistance, feel free to reach out to our support team.</p>"
                message_content += "<p class='card-text'>Thank you for choosing Spark!</p>"
                message_content += "<p class='card-text'>Best regards,<br>Spark Team</p>"

                msg = Message(recipients=[recipient], html=message_content, subject=subject)
                conn.send(msg)

    return {'message': "Daily reminder to users executed"}


@celery.task()
def monthly_report():
    sponsors = Sponsor.query.all()

    if sponsors:
        with mail.connect() as conn:
            subject = "Monthly Activity Report"

            for sponsor in sponsors:
                campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
                campaign_details = []
                for campaign in campaigns:
                    ad_requests = AdRequest.query.filter_by(campaign_id=campaign.id).all()
                    ads_done = len(ad_requests)
                    budget_used = sum(ad.payment_amount for ad in ad_requests)
                    budget_remaining = campaign.budget - budget_used

                    campaign_details.append({
                        'name': campaign.name,
                        'ads_done': ads_done,
                        'budget_used': budget_used,
                        'budget_remaining': budget_remaining,
                    })

                message_content = "<h1 class='card-title text-success'>Monthly Activity Report</h1>"
                message_content += f"<p class='card-text'>Hello, {sponsor.user.username}&nbsp;! Here is your monthly activity report.</p>"
                for detail in campaign_details:
                    message_content += f"<h2>Campaign Name: {detail['name']}</h2>"
                    message_content += f"<p>Advertisements Done: {detail['ads_done']}</p>"
                    message_content += f"<p>Budget Used: {detail['budget_used']}</p>"
                    message_content += f"<p>Budget Remaining: {detail['budget_remaining']}</p>"

                message_content += "<p class='card-text mt-3'>If you have any questions or need assistance, feel free to reach out to our support team.</p>"
                message_content += "<p class='card-text'>Thank you for choosing Spark!</p>"
                message_content += "<p class='card-text'>Best regards,<br>Spark Team</p>"

                msg = Message(recipients=[sponsor.user.email], html=message_content, subject=subject)
                conn.send(msg)

    return {'message': "Monthly report to sponsors executed"}


@celery.task()
def user_triggered_async_job(user_id):
    sponsor_id = Sponsor.query.filter_by(user_id=user_id).first().id
    if not sponsor_id:
        raise ValueError("Sponsor not found")
    campaigns = Campaign.query.with_entities(
        Campaign.name, Campaign.description, Campaign.start_date, Campaign.end_date, Campaign.budget, Campaign.goals
    ).filter_by(sponsor_id=sponsor_id).all()

    if not campaigns:
        raise ValueError("No campaigns found for the given sponsor")

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['name', 'description', 'start date', 'end date', 'budget', 'goals'])

    for campaign in campaigns:
        csv_writer.writerow(
            [campaign.name, campaign.description, campaign.start_date, campaign.end_date, campaign.budget,
             campaign.goals])

    base_dir = os.path.abspath(os.path.dirname(__name__))
    csv_file_path = os.path.join(base_dir, 'campaigns_{}.csv'.format(user_id))
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_buffer.getvalue())

    time.sleep(3)
    return csv_buffer.getvalue()


celery.conf.beat_schedule = {
    'my_monthly_task': {
        'task': "app.monthly_report",
        'schedule': crontab(hour=13, minute=50, day_of_month=1,
                            month_of_year='*/1'),
        # 'schedule': crontab(),
    },
    'my_daily_task': {
        'task': "app.daily_reminder",
        'schedule': crontab(hour=12, minute=12),
        # 'schedule': crontab(),
    },
}


# ----------- Async Job will trigger here ---------------#
class AsyncJobResource(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            csv_data = user_triggered_async_job(user_id)

            response = make_response(csv_data)

            response.headers['Content-Disposition'] = 'attachment;filename=campaign_report.csv'

            response.headers['Content-type'] = 'text/csv'

            return response
        except Exception as e:
            return jsonify(str(e)), 500


api.add_resource(AsyncJobResource, '/api/report/data/<int:user_id>')


# class DownloadResource(Resource):
#     @jwt_required()
#     def get(self, task_id):
#         res = AsyncResult(task_id)
#         if res.ready():
#             return jsonify({"result": res.result}), 200
#         return jsonify({"message": "Task is not ready"}), 202
#
# api.add_resource(DownloadResource, '/api/report/download/<string:task_id>')

# class SendWarningResource(Resource):
#     @jwt_required()
#     def get(self):
#         managers = User.query.filter_by(role='manager').all()
#         man_list = []
#         for man in managers:
#             man_data = {
#                 'id': man.id,
#                 'name': man.name,
#                 'email': man.email,
#             }
#             man_list.append(man_data)
#         return man_list, 200
#
#     def post(self):
#         data = request.get_json()
#         with mail.connect() as conn:
#             subject = "Alert from Admin"
#             message = data['message']
#             msg = Message(recipients=[data['email']],
#                           html=message, subject=subject)
#             conn.send(msg)
#
#             return jsonify({'message': "sent"}), 200
#
#
# api.add_resource(SendWarningResource, '/send/alert')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
