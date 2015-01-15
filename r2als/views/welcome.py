from pyramid.view import view_config
from r2als import models

import datetime

import mongoengine as me

@view_config(route_name='index', renderer='/welcome/index.mako')
def index(request):
	
    return dict(
                test_text = "Hello wolrd!"
                )
