
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from app.api import auth_routes, user_routes, event_routes, category_routes, invitation_routes, attendee_routes, speaker_routes, admin_routes, org_routes
from app.db import base, session
load_dotenv()
USER_NAME = os.getenv("USER_NAME")
# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
# Create database tables
base.Base.metadata.create_all(bind=session.engine)
app = FastAPI(title="IntraHub API")
# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(event_routes.router, prefix="/events", tags=["events"])
app.include_router(category_routes.router, prefix="/categories", tags=["categories"])
app.include_router(invitation_routes.router, prefix="/invitations", tags=["invitations"])
app.include_router(attendee_routes.router, prefix="/attendees", tags=["attendees"])
app.include_router(speaker_routes.router, prefix="/speakers", tags=["speakers"])
app.include_router(admin_routes.router, prefix="/admins", tags=["admins"])

app.include_router(org_routes.router, prefix="/orgs", tags=["orgs"])


