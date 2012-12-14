# -*- coding: utf-8 -*-
# This plugins is licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
# Authors: Kenji Hosoda <hosoda@s-cubism.jp>
from gluon import *
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


    
class LikertWidget(object):

    def __init__(self):
        settings = self.settings = Storage()
        settings.files = None

    def __call__(self, field, value, **attributes):
        if self.settings.files is None:
            _files = [URL(APP, 'static', 'plugin_kibit_widgets/kibit_widgets.css'),
                      URL(APP, 'static', 'plugin_kibit_widgets/jquery.kibit_widgets.js')]
        else:
            _files = self.settings.files
        _set_files(_files)
        
        table=SQLFORM.widgets.radio.widget(field, value, **attributes)
        
        labels = TR(*[TH(td.components[1]) for td in table.elements('td')])
        options_fields = TR(*[TD(td.element('input')) for td in table.elements('td')])
        
        new_table = DIV(TABLE(labels, options_fields, **table.attributes), _class='likert_box')
                
        return new_table
    
class SmileyWidget(object):

    def __init__(self):
        settings = self.settings = Storage()
        settings.files = None

    def __call__(self, field, value, **attributes):
        if self.settings.files is None:
            _files = [URL(APP, 'static', 'plugin_kibit_widgets/kibit_widgets.css'),
                      URL(APP, 'static', 'plugin_kibit_widgets/jquery.kibit_widgets.js')]
        else:
            _files = self.settings.files
        _set_files(_files)
        
        header_row = DIV(*[IMG(_src=URL('static', 'plugin_kibit_widgets/smiley_%s.PNG' % i), _class='smiley_header_%s' % i) for i in range(1,6)], _class='header')
        slider_row = DIV(INPUT(_name=field.name,
                 _id="%s_%s" % (field._tablename, field.name),
                 _class=field.type,
                 _value=value,
                 requires=field.requires), DIV(_class='slider'))
        
        new_table = DIV(header_row, slider_row, _class='smiley_box')
                
        return new_table