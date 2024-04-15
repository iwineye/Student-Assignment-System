#IMPORTING LIBRARIES

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, current_user
from functools import wraps
from flask_restful import Resource, Api

#INITIALISING AND SECURE CREDENTIALS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/assignments'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#CREATED INSTANCES
db = SQLAlchemy(app)
jwt = JWTManager(app)
api=Api(app)

#DECLARING TABLES

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    grade = db.Column(db.String(10), nullable=True)
    assignment_link = db.Column(db.String(200), nullable=True)

## TO ADD SUPER SPECIAL ACCESS
#def add_superuser():
#    superuser = User(username='TEACHER_02', password='CLASS', is_superuser=True)
#    db.session.add(superuser)
#    db.session.commit()
    
## TO GET USER DETAILS FROM ID
#def get_user_by_id(id):
#    return User.query.filter_by(id=id).first()

# DECORATOR TO ENSURE THE USER IS A SUPERUSER
def superuser_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user.is_superuser:
            return jsonify({'error': 'Unauthorized'}), 403
        return fn(*args, **kwargs)
    return wrapper

## USER REGISTRATION 
class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']

        if not username or not password:
            return{'message':'Missing username or password'}, 400
        if User.query.filter_by(username=username).first():
            return{'message':'username taken'},400
            
        new_user=User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return{'message':"user_created_successfully"},200

## USER LOGIN WITH AUTHENTICATION
    
class UserLogin(Resource):  
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        user= User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            access_token = create_access_token(identity=user.id)

            return{'access_token':access_token},200 

        return{'message':"invalid credentials"},401


## TO CREATE ASSIGNMENT ACCESSABLE TO ONLY SUPER USER

@app.route('/create_assignment', methods=['POST'])
@jwt_required()
@superuser_required
def create_assignment():
    data = request.json
    if not all(key in data for key in ['input_user_id','subject', 'description', 'due_date']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    ##INPUTS OF ASSIGNMENTS

    input_user_id = data['input_user_id']
    subject = data['subject']
    description = data['description']
    due_date = data['due_date']
    
    user = User.query.get(input_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    ##ASSIGN VALUES TO DB

    assignment = Assignment(
        user_id=user.id,
        user_name=user.username,
        subject=subject,
        description=description,
        due_date=due_date,
        grade=None,
        assignment_link=None
    )
    db.session.add(assignment)
    db.session.commit()
    
    return jsonify({'message': 'Assignment created successfully'}), 201




## TO LOAD THE USER BY USER ID
def load_user(user_id):
    return User.query.get(user_id)


# REGISTER USER LOADER FUNCTION
@jwt.user_lookup_loader
def user_loader_callback(jwt_header, jwt_payload):
    user_id = jwt_payload['sub']
    return load_user(user_id)

#  TO DELETE ASSIGNMENTS 

@app.route('/assignments/<int:id>', methods=['DELETE'])
@jwt_required()
@superuser_required
def delete_assignment(id):
    if not current_user.is_superuser:
        return jsonify({'error': 'Unauthorized'}), 403

    assignment = Assignment.query.filter_by(id=id).first()
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
        
    db.session.delete(assignment)
    db.session.commit()
        
    return jsonify({'message': 'Assignment deleted successfully'})

## TO VIEW THE ASSIGNMENTS FOR NORMAL USERS

@app.route('/assignments', methods=['GET'])
@jwt_required()
def get_assignments():
    current_user_id = get_jwt_identity()
    assignments = Assignment.query.filter_by(user_id=current_user_id).all()
    assignment_list = []
    for assignment in assignments:
        assignment_data = {
            'user_name': assignment.user_name,
            'subject': assignment.subject,
            'description': assignment.description,
            'due_date': assignment.due_date.strftime('%Y-%m-%d')  # Format date as string
        }
        assignment_list.append(assignment_data)
    return jsonify({'assignments': assignment_list}), 200



##DECLARING LOGIN AND RESITRATION ROUTES 

api.add_resource(UserLogin,'/login')
api.add_resource(UserRegistration,'/register')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #add_superuser()
    app.run(debug=True)