# -*- coding: utf-8 -*-
from gluon.custom_import import track_changes; track_changes(True) #todo: raus, wenn man online geht.
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################


db.define_table("questions", 
                Field('title', 'string'))

db.define_table("answers",
                Field("itemID", db.questions, requires = IS_IN_DB(db,db.questions.id,'%(title)s', error_message=T('Bitte wählen Sie eine Frage aus')), label = T('Frage')),
                Field('scale', 'integer', requires=IS_IN_SET({1:T('Trifft gar nicht zu'),2:T('Trifft nicht zu'), 3:T('teils-teils'), 4:T('Trifft zu'), 5:T('Trifft total zu')})))


db.define_table("answers_smiley",
                Field("itemID", db.questions, requires = IS_IN_DB(db,db.questions.id,'%(title)s', error_message=T('Bitte wählen Sie eine Frage aus')), label = T('Frage')),
                Field('scale', 'integer', requires=IS_IN_SET(range(1,6))))

db.define_table('answers_stars',
    Field('rating', 'integer',
          requires=IS_IN_SET(range(1, 6)),  # "requires" is necessary for the rating widget
))


db.answers_stars.rating.represent = lambda v: \
    DIV(*[SPAN("", _class='star-rating-represent-full') if i<=v else SPAN("", _class='star-rating-represent-empty') for i in range(1,6)])

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
