from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField
)
from wtforms.validators import DataRequired

class PostItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image_url = StringField('Image Upload', validators=[DataRequired])
    submit = SubmitField('Save')