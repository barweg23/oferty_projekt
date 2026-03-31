from wtforms import Form, StringField, validators, IntegerField


class AdditionalExpanses(Form):
    koszty_dodatkowe = StringField('koszty_dodatkowe', [validators.Length(min=4, max=50)])
    cena = IntegerField('cena', [validators.NumberRange(min=0, max=60000000)])
