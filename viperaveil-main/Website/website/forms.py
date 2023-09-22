from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, HiddenField
from wtforms.fields.choices import SelectMultipleField
# from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import (
    InputRequired,
    # Email,
    # EqualTo,
    Length,
    # URL,
    # ValidationError
)
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import (
    TextArea,
    # ListWidget,
    CheckboxInput,
    ColorInput
)

from markupsafe import Markup
from wtforms.widgets import html_params


class ListGrid:
    def __init__(self, html_tag="ul"):
        self.html_tag = html_tag

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = ["<{} class='row p-0 m-0' style='height:auto;' {}>".format(
            self.html_tag, html_params(**kwargs))]
        for subfield in field:
            html.append(
                f"<li class='col-md-4 d-block' style='list-style-type:none;'>{subfield()} {subfield.label}</li>")

        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))


class MultiCheckboxField(SelectMultipleField):
    widget = ListGrid()
    option_widget = CheckboxInput()


TEXTURE_LABELS = [
    ('decal', 'Decal'),
    ('topper', 'Topper'),
    ('antenna', 'Antenna'),
    ('ball', 'Ball'),
    ('goal', 'Goal')]
PRESET_LABELS = [
    ('striker', 'Striker'),
    ('defense', 'Defense'),
    ('dribble', 'Dribble'),
    ('air-dribble', 'Air-Dribble'),
    ('challenge', 'Challenge'),
    ('race', 'Race')]


class ItemSearchForm(FlaskForm):
    type = SelectField('type', [InputRequired()], choices=[
        ('All', 'All'),
        ('texture', 'Textures'),
        ('preset', 'Presets')
    ])
    search = StringField('')

    texture_filters = MultiCheckboxField(
        "texture-filters", choices=TEXTURE_LABELS)
    preset_filters = MultiCheckboxField(
        "preset-filters", choices=PRESET_LABELS)

    order_by = SelectField('order-by', [InputRequired()], choices=[
        ('downloads', 'Downloads'),
        ('likes', 'Likes'),
        ('oldest', 'Oldest'),
        ('newest', 'Newest'),
        ('recently updated', 'Recently Updated')
    ])

    decal = BooleanField()
    topper = BooleanField()
    antenna = BooleanField()
    ball = BooleanField()
    goal = BooleanField()

    striker = BooleanField()
    defense = BooleanField()
    dribble = BooleanField()
    air_dribble = BooleanField()
    challenge = BooleanField()
    race = BooleanField()

    submit_button = SubmitField('Search')


class ItemUploadForm(FlaskForm):
    type = HiddenField('Type')
    title = StringField('Title', validators=[InputRequired(
    ), Length(-1, 128)], render_kw={"placeholder": "Enter Title"})

    textureLabels = SelectField(
        'Type Label',
        choices=[
            ('',
             '')] +
        TEXTURE_LABELS,
        default=None,
        validate_choice=False)
    presetLabels = SelectField(
        'Type Label',
        choices=[
            ('',
             '')] +
        PRESET_LABELS,
        default=None,
        validate_choice=False)

    description = StringField('Description', widget=TextArea(), validators=[
                              InputRequired(), Length(-1, 512)], render_kw={"placeholder": "Enter Description"})

    # collection = StringField('Collection', render_kw={"placeholder": "Enter Collection Name"})
    collection = SelectField('Collection', default=None)

    previewImage = FileField('Display Image', validators=[InputRequired(
    ), FileAllowed(['png', 'jpg'], "Image format must be .png or .jpg")])
    file = FileField(
        'Zip File',
        validators=[
            InputRequired(),
            FileAllowed(
                ['zip'],
                "File format must be .zip")])

    submit_button = SubmitField('Submit')


class ItemActions(FlaskForm):
    likeItem_button = SubmitField('Like Item')


class AddCollection(FlaskForm):
    collection_title = StringField('Collection Title', validators=[InputRequired(
    ), Length(-1, 64)], render_kw={"placeholder": "Enter Collection Name"})
    collection_colour = StringField(widget=ColorInput(), default='#8000ff')
    collection_submit_button = SubmitField('Submit')
