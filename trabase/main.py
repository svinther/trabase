import flask_login
from flask_login import login_required

from flask import current_app as app, flash, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField
from wtforms.validators import DataRequired


class ReportGeneratorForm(FlaskForm):
    transformer_id = StringField('Transformer Id',validators=[DataRequired(message=('Please enter a valid transformer id'))])
    database_file = FileField('Samples database file (xlsx)', validators=[FileRequired("Please provide database")])


@app.route('/', methods=["GET", "POST"])
@login_required
def main():
    if request.method == "GET":
        return render_template('main.html', form=ReportGeneratorForm(), current_user=flask_login.current_user.email)

    report_form = ReportGeneratorForm()
    if report_form.validate_on_submit():
        database_filename = secure_filename(report_form.database_file.data.filename)
        database_stream =  report_form.database_file.data.stream
        #parse with pandas like pandas.read(database_stream)

        transformer_id = request.form.get('transformer_id')

        return "Thank you %s - we will process your file for sure. (%s / %s)" %(flask_login.current_user.name, transformer_id, database_filename)

    flash('Form upload error')
    return redirect(url_for('main'))


