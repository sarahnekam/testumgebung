#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from gluon import *
from gluon import current
from gluon.dal import DAL, Field
from gluon.sqlhtml import SQLFORM
from gluon.validators import IS_NOT_EMPTY, IS_EMAIL, IS_LENGTH, IS_IN_SET
from gluon.storage import Storage

# For referencing static and views from other application
import os
APP = os.path.basename(os.path.dirname(os.path.dirname(__file__)))


def _set_files(files):
        if current.request.ajax:
            current.response.js = (current.response.js or '') + """;(function ($) {
    var srcs = $('script').map(function(){return $(this).attr('src');}),
        hrefs = $('link').map(function(){return $(this).attr('href');});
    $.each(%s, function() {
        if ((this.slice(-3) == '.js') && ($.inArray(this.toString(), srcs) == -1)) {
            var el = document.createElement('script'); el.type = 'text/javascript'; el.src = this;
            document.body.appendChild(el);
        } else if ((this.slice(-4) == '.css') && ($.inArray(this.toString(), hrefs) == -1)) {
            $('<link rel="stylesheet" type="text/css" href="' + this + '" />').prependTo('head');
            if (/* for IE */ document.createStyleSheet){document.createStyleSheet(this);}
    }});})(jQuery);""" % ('[%s]' % ','.join(["'%s'" % f.lower().split('?')[0] for f in files]))
        else:
            current.response.files[:0] = [f for f in files if f not in current.response.files]
 
 
class Mainfeedback(object):
    """Build a Feedback object"""

     
    def __init__(self, db, heading, feeling_choose, feeling_error, message_error):
        self.db = db
        
        self.translations = {"feeling_choose": feeling_choose, "feeling_error": feeling_error, "message_error": message_error}
        
        self.session = current.session
        self.request = current.request
        self.response = current.response
        self.cache = current.cache
        self.define_table()
        self.set_validators()
        
        settings = self.settings = Storage()
        settings.files = None
        
        if self.settings.files is None:
            _files = [URL(APP, 'static', 'plugin_feedbacks/plugin_feedbacks.css'),
                      URL(APP, 'static', 'plugin_feedbacks/plugin_feedbacks.js')]
        else:
            _files = self.settings.files
        _set_files(_files)
        

     
    def define_table(self):
        self.mainfeedback = self.db.define_table("mainfeedback",
        Field("feeling", "string"),
        Field("message", "string")
        )
     
    def set_validators(self):
        self.mainfeedback.feeling.requires = IS_IN_SET(['1','2'],zero=self.translations['feeling_choose'], error_message=self.translations['feeling_error'])
        self.mainfeedback.message.requires = IS_LENGTH(140,1, error_message=self.translations['message_error'])
     
    def form(self, formstyle):   
        
        form = SQLFORM(self.mainfeedback, formstyle=formstyle).process()
        
        return form
     
    def load(self, scope, limitby=None):
        queries = {"all": self.mainfeedback.id>0, "happy": self.mainfeedback.feeling==1, "unhappy": self.mainfeedback.feeling==2}
        return self.db(queries[scope]).select(limitby=limitby)