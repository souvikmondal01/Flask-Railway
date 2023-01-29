from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/crudApp"
DB_URL = "postgresql://postgres:KSynoUCoxXSMyEoxjn1B@containers-us-west-182.railway.app:7392/railway"
SECRET_KEY = "yoursecretkey"

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.secret_key = SECRET_KEY
db.init_app(app)
print("DB Initialized Successfully")

with app.app_context():
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        username = db.Column(db.String(200), nullable=False)
        email = db.Column(db.String(200), nullable=False)
        password = db.Column(db.String(200), nullable=False)

    @app.route('/')
    def index():
        return jsonify(name="Souvik Mondal")

    @app.route("/hello", methods=["GET"])
    def hello():
        return jsonify(msg="hello world")

    @app.route("/signup", methods=["POST", "GET"])
    def signup():

        new_user = User(
            name=request.form["name"],
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"]
        )
        user = User.query.filter_by(email=new_user.email).first()
        if user:
            return "user already exists"
        else:
            username = User.query.filter_by(
                username=new_user.username).first()
            if username:
                return "username already exists"
            else:
                db.session.add(new_user)
                db.session.commit()
                return "user added successfully"

    @app.route("/login", methods=["POST"])
    def login():
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return "login successful"
        elif user and user.password != password:
            return "invalid credentials"
        else:
            return "user does not exist"

    @app.route("/get_user", methods=["GET"])
    def get_user():
        users = User.query.all()

        user_data = {}
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "email": user.email
            })
        user_data["users"] = user_list

        return jsonify(user_data)

    # db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
