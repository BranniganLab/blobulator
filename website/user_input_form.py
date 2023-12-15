from wtforms import Form, FloatField, validators, StringField, FieldList
from math import pi
from wtforms.widgets import TextArea

"""
This creates the forms neccessary for the tool using the wtforms module
"""


def my_length_check(form, field):
    if len(field.data) > 2:
        raise ValidationError('Field must be less than 50 characters')

class InputForm(Form):
    uniprot_id = StringField(
        label='Uniprot ID:', widget=TextArea(), default='P37840',
        validators=[validators.InputRequired(), my_length_check])
    ensembl_id = StringField(
        label='Ensembl ID:', widget=TextArea(), default='ENSG00000145335', 
        validators=[validators.InputRequired(), my_length_check])
    aa_sequence = StringField(
        label='Sequence:', widget=TextArea(), default='MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATVAEKTKEQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFVKKDQLGKNEEGAPQEGILEDMPVDPDNEAYEMPSEEGYQDYEPEA',
        )
    seq_name = StringField(
        label='Seq name:', widget=TextArea(), default='Sequence Name',
        )
    def validate_name(form, field):
        if len(field.data) > 3:
            raise ValidationError('Name must be less than 50 characters')
