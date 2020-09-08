from flask import jsonify, request, session, url_for
import uuid
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from werkzeug.utils import redirect

from src.DB.db import my_db, nurse_details_col


class NurseUser:
    def __init__():
        self.id = None
        self.email = None
        #etc...
    
    @classmethod
    def get_nurse(name):
        query = {"name": name}
        result_doc = nurse_details_col.find_one(my_query)
        return NurseUser(result_doc.id, result_doc.email)
    
    @classmethod
    def get_all_nurses_names():
        all_nurses = []
        nurses_names = nurse_details_col.find({}, {"name"})
        for nurse in nurses_names:
            all_nurses.append(nurse)
        return all_nurses
        
    def start_session(self, userId):
        session['logged in'] = True
        session['user'] = userId
        return jsonify(userId), 200

    def login(self):
        user_id = my_db.users_col.find_one({'email': request.form.get(
            'email')})  # TODO: fix save the data from register murse in the db so this method will work
        # if user and pbkdf2_sha256.verfiy(request.form.get('password'), user['id_num']):
        return self.start_session(user_id)
        # return jsonify({"error", "invalid email or password"}), 401

    def logout(self):
        session.clear()
        return redirect(url_for('login'))

    def register_nurse(self):
        # Create the user object
        user = {"_id": uuid.uuid4().hex,
                "email": request.form.get('email'),
                "id_num": request.form.get('id_num'),
                "courses": request.form.get('courses'),
                "name": request.form.get('name'),
                "roles": request.form.get('roles'),
                "work_years": request.form.get('work_years'),
                "employment_percentage": request.form.get('employment_percentage'),
                }
        # Encrypt the password
        user['id_num'] = pbkdf2_sha256.encrypt(user['id_num'])
        return self.start_session(user)
       


    def get_is_admin(self):
        pass
