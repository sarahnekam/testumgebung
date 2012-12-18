# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from plugin_kibit_widgets import LikertWidget
from plugin_kibit_widgets import SmileyWidget
from plugin_rating_widget import RatingWidget
import plugin_feedbacks

db.answers.scale.widget = LikertWidget()
db.answers_smiley.scale.widget = SmileyWidget()
db.answers_stars.rating.widget = RatingWidget()
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    """


    form = SQLFORM(db.answers)
    
    form2 = SQLFORM(db.answers_smiley)
    
    form3 = SQLFORM(db.answers_smiley)
    
    form4 = SQLFORM(db.answers_stars)
    
    stars_results = db(db.answers_stars.id > 0).select()
    
    mainfeedbackform_translations = {"heading": T("KI.EVA macht mich [FEELING], weil ..."),
                                     "feeling_choose": T("Bitte auswählen"),
                                     "feeling_error": T("Bitte eine Emotion auswählen"),
                                     "message_error": T("Bitte zwischen 1 und 140 Zeichen eintragen.")}
    mainfeedbackObject = plugin_feedbacks.Mainfeedback(db, **mainfeedbackform_translations)
    mf_form = mainfeedbackObject.form(formstyle='divs')


    return dict(message=T('Hello World'), form=form, form2=form2, form3=form3, form4=form4, stars_results=stars_results, mf_form=mf_form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
