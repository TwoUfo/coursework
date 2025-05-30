from flask import request, session, make_response
from flask_restx import Namespace, Resource, fields

from adapters.input.api.auth.security import (
    generate_jwt,
    hash_password,
    login_required,
    set_cookie,
    verify_password,
)
from adapters.input.api.auth.utils import get_session_id, get_user_by_email
from adapters.output.persistence.sqlalchemy.models.user import UserModel
from infrastructure.database import db

api = Namespace("auth", description="Authentication operations")

# API Models
login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password")
})

register_model = api.model("Register", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
    "is_admin": fields.Boolean(required=False, description="Admin status")
})


@api.route("/register")
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """Register a new user."""
        data = request.get_json()
        
        if get_user_by_email(data["email"]):
            return {"message": "Email already registered"}, 400
        
        user = UserModel(
            email=data["email"],
            password_hash=hash_password(data["password"]),
            is_admin=data.get("is_admin", False)
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201


@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and create session."""
        data = request.get_json()
        
        user = get_user_by_email(data["email"])
        if not user:
            return {"message": "User not found"}, 404
            
        if not verify_password(data["password"], user.password_hash):
            return {"message": "Invalid password"}, 401
        
        # Set session data
        session["user_id"] = user.id
        session["email"] = user.email
        session["is_admin"] = user.is_admin
        
        # Generate tokens
        session_id = get_session_id()
        access_token = generate_jwt(session_id, expires_in=3600)  # 1 hour
        refresh_token = generate_jwt(session_id, expires_in=604800)  # 1 week
        
        # Create response
        response = make_response({"message": "Login successful", "user": user.to_dict()})
        response.status_code = 200
        
        # Set cookies
        response = set_cookie(response, "access_token", access_token)
        response = set_cookie(response, "refresh_token", refresh_token)
        
        return response


@api.route("/logout")
class Logout(Resource):
    @login_required
    def post(self):
        """Clear user session and cookies."""
        session.clear()
        
        response = make_response({"message": "Logout successful"})
        response.status_code = 200
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return response


@api.route("/refresh")
class TokenRefresh(Resource):
    def post(self):
        """Refresh access token using refresh token."""
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return {"message": "Refresh token required"}, 401
            
        payload = decode_jwt(refresh_token)
        if not payload:
            return {"message": "Invalid or expired refresh token"}, 401
            
        session_id = payload.get("session_id")
        if not session_id or session_id != session.get("session_id"):
            return {"message": "Invalid session"}, 401
            
        # Generate new access token
        access_token = generate_jwt(session_id, expires_in=3600)
        
        # Create response
        response = make_response({"message": "Token refreshed successfully"})
        response.status_code = 200
        response = set_cookie(response, "access_token", access_token)
        
        return response 