import os
import random
from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, validators

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    WTF_CSRF_ENABLED=False,
)

admin_min = 1
admin_max = 10

admin_seed = os.environ["SECRET_SEED"]
random.seed(admin_seed)
admin_number = random.randint(admin_min, admin_max)
admin_number = str(admin_number)

class NumberForm(FlaskForm):
	usr_number = IntegerField(label="usr_number", validators=[
		validators.NumberRange(min=admin_min, max=admin_max, message="out of range"),
		validators.InputRequired(message="no input")
	])


@app.route("/", methods=["GET", "POST"])
def home():
	if request.method == "POST":
		print(request.form["usr_number"])
		print(admin_number)
		form = NumberForm(request.form)
		print(form.validate())
		if form.validate():
			request_data = request.form["usr_number"]
			if request_data == admin_number:
				return f"= {request_data} is true!", 200
			elif request_data > admin_number:
				return f"{request_data} > ?", 200	
			else:
				return f"{request_data} < ?", 200
		else:
			return "Wrong input"

	if request.method == "GET":
		return "GET", 200


if __name__ == "__main__":
    app.run()
