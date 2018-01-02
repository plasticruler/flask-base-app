from flask import Flask
from wtforms import Form, Field, TextField

from wtforms.widgets import TextInput, html_params


def render_datetime_widget(field, **kwargs):
    kwargs.setdefault('id',field.id)    
    html = """<div class='input-group date datetimepicker' id='{}'> 
                    <input type='text' class="form-control" />
                    <span class="input-group-addon">
                        <span class="glyphicon glyphicon-calendar"></span>
                    </span>
                </div>                
                """.format(field.id)
    return html
