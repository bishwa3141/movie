from pyramid.response import Response
from pyramid.view import view_config

import urllib2
import json

from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from .models import (
    DBSession,
    Movie,
    )


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    search_url = ''
    if 'form.submitted' in request.params:
        data = request.params['body']
        search_url = request.route_url('search', name = data)
        return HTTPFound(location = request.route_url('search',
                                                      name = data))

    return dict(search_url= search_url)


@view_config(route_name='search', renderer='templates/search.pt')
def search(request):
    movie_name = request.matchdict['name']
    new_name = movie_name.replace(" " , '+')
    response = urllib2.urlopen('http://www.omdbapi.com/?t=' + new_name + '&y=&plot=short&r=json')
    data = json.load(response)
    name = data['Title']
    photo_link = data['Poster']
    return dict(name=name, poster = photo_link)
    



conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_ProjectIMDB_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

