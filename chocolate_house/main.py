from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chocolate_house.db"
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to your own secret key
db = SQLAlchemy(app)

class SeasonalFlavor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer)

class CustomerSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suggestion = db.Column(db.Text, nullable=False)

class AllergyConcern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concern = db.Column(db.Text, nullable=False)

# Ingredient form for validation
class IngredientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add Ingredient')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/seasonal-flavors", methods=["GET", "POST"])
def seasonal_flavors():
    if request.method == "POST":
        flavor = SeasonalFlavor(name=request.form["name"], description=request.form["description"], ingredients=request.form["ingredients"])
        db.session.add(flavor)
        db.session.commit()
    flavors = SeasonalFlavor.query.all()
    return render_template("seasonal_flavors.html", flavors=flavors)

@app.route("/delete-flavor/<int:flavor_id>", methods=["POST"])
def delete_flavor(flavor_id):
    flavor = SeasonalFlavor.query.get_or_404(flavor_id)
    db.session.delete(flavor)
    db.session.commit()
    return redirect(url_for('seasonal_flavors'))

@app.route('/ingredient-inventory', methods=['GET', 'POST'])
def ingredient_inventory():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        new_ingredient = Ingredient(name=name, quantity=quantity)
        db.session.add(new_ingredient)
        db.session.commit()
        return redirect(url_for('ingredient_inventory'))  # Redirect to the same page to show the updated list

    ingredients = Ingredient.query.all()  # Retrieve all ingredients
    return render_template('ingredient_inventory.html', ingredients=ingredients)


@app.route("/delete-ingredient/<int:ingredient_id>", methods=["POST"])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for('ingredient_inventory'))

@app.route("/customer-suggestions", methods=["GET", "POST"])
def customer_suggestions():
    if request.method == "POST":
        suggestion = CustomerSuggestion(suggestion=request.form["suggestion"])
        db.session.add(suggestion)
        db.session.commit()
    suggestions = CustomerSuggestion.query.all()
    return render_template("customer_suggestions.html", suggestions=suggestions)
@app.route("/allergy-concerns", methods=["GET", "POST"])
def allergy_concerns():
    if request.method == "POST":
        concern = request.form["concern"].strip().lower()  # Normalize input for matching
        # Save the concern to the database
        new_concern = AllergyConcern(concern=concern)
        db.session.add(new_concern)
        db.session.commit()

        # Now check for flavors that contain ingredients matching the concern
        flavors_with_allergens = SeasonalFlavor.query.filter(
            SeasonalFlavor.ingredients.ilike(f"%{concern}%")
        ).all()

        # Print the matched flavors for debugging
        print(f"Flavors with allergens related to '{concern}': {[flavor.name for flavor in flavors_with_allergens]}")

        return render_template("allergy_concerns.html", concerns=AllergyConcern.query.all(),
                               flavors=flavors_with_allergens, concern=concern)

    concerns = AllergyConcern.query.all()
    return render_template("allergy_concerns.html", concerns=concerns)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)