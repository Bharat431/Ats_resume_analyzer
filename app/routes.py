"""API routes for ATS Resume Agent"""

from flask import Blueprint, request, jsonify
from app.services.evaluation_service import evaluate

api_bp = Blueprint('api', __name__, url_prefix='/api')