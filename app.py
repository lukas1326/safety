from flask import Flask, render_template, request,url_for,g,flash
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField

app = Flask (__name__)
app.config["SECRET_KEY"] = "secretkey"

class NewItemForm(FlaskForm):
    observe = StringField("Observation")
    bad_case = StringField("Bad cases")
    obs_period = TextAreaField("Observe period")
    req = SelectField("Pravilo")
    procedure = SelectField("Procedure")
    submit = SubmitField("Submit")

@app.route("/", methods=["GET","POST"])
def home():
    conn = get_db()
    c = conn.cursor()
    form = NewItemForm()

    c.execute("SELECT id, name FROM reqs")
    reqs = c.fetchall()
    form.req.choices = reqs

    c.execute("""SELECT id, name FROM procedures
                    WHERE req_id = ?""",
                    (1,)
    )
    procedures = c.fetchall()
    form.procedure.choices = procedures

    if request.method == "POST":
        # Process the form data
        c.execute("""INSERT INTO monitor
                    (observe, bad_case, obs_period, req_id, procedure_id, department_id,position_id)
                        VALUES (?,?,?,?,?,?,?)""",
                        (
                            form.observe.data,
                            form.bad_case.data,
                            form.obs_period.data,
                            "",
                            form.req.data,
                            form.procedure.data,
                            1
                        )
        )
        conn.commit()
        flash("Item {} has been successfully submitted".format(request.form.get("observe")),"success")
    return render_template ("home.html",form=form)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db/safety.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
