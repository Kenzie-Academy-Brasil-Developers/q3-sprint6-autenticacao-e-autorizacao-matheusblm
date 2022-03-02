from flask import Blueprint
from app.controllers.user_controller import sign_in, sign_up, get_user, update_user, delete_user

bp_user = Blueprint("bp_user", __name__, url_prefix="/api")

bp_user.post("/signup")(sign_up)
bp_user.post("/signin")(sign_in)
bp_user.get("")(get_user)
bp_user.put("")(update_user)
bp_user.delete("")(delete_user)