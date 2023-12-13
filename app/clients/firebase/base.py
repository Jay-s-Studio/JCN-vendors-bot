"""
Base Firebase Client
"""
import firebase_admin
from firebase_admin import credentials

from app.config import settings

cred = credentials.Certificate(settings.GOOGLE_FIREBASE_CERTIFICATE)
firebase_app = firebase_admin.initialize_app(cred)
