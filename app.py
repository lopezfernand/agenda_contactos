from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://agenda_user:agenda_pass@db:5432/agenda_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)
    correo = db.Column(db.String(120))
    direccion = db.Column(db.String(200))


@app.route("/")
def home():
    contactos = Contacto.query.all()
    return render_template("index.html", contactos=contactos)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        contacto = Contacto(
            nombre=request.form["nombre"],
            telefono=request.form["telefono"],
            correo=request.form["correo"],
            direccion=request.form["direccion"]
        )
        db.session.add(contacto)
        db.session.commit()
        return redirect("/")

    return render_template("nuevo_contacto.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)