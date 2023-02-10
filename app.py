"""Flask app for Cupcakes"""

from flask import Flask,request,jsonify,render_template
from flask_cors import CORS

from models import db, connect_db, Cupcake


app=Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']="postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True
app.config['SECRET_KEY'] = 'secretsecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


with app.app_context():
    connect_db(app)
    db.create_all()

@app.route("/")
def home():
    """render homepage"""
    cupcakes=Cupcake.query.all()
    return render_template("home.html",cupcakes=cupcakes)

@app.route("/api/cupcakes")
def show_cupcakes():
    """show list of cupcakes (returns json data of cupcake object"""

    cupcakes=[cupcake.to_dict() for cupcake in Cupcake.query.all()]
    
    
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes",methods=['POST'])
def add_cupcake():
  
    new_cupcake=Cupcake(flavor=request.json.get('flavor'),size=request.json.get('size'),rating=request.json.get('rating'),image=request.json.get('image'))
                   
    with app.app_context():
        db.session.add(new_cupcake)
        db.session.commit()

        return(jsonify(new_cupcake=new_cupcake.to_dict()),201)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_info(cupcake_id):
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())
   

@app.route('/api/cupcakes/<int:cupcake_id>',methods=["PATCH","GET"])
def update_cupcake(cupcake_id):

    cupcake=Cupcake.query.get_or_404(cupcake_id)
    
    #cupcake.id=request.json['id'],
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    with app.app_context():
       
        db.session.commit()
    
        return jsonify(cupcake=cupcake.to_dict())



@app.route('/api/cupcakes/<int:cupcake_id>',methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")




