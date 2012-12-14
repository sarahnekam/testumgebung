db.define_table('plugin_feedbacks_feedback',
   Field("feeling", "string",label=T("Gefühl")),
   Field("message", "text", label=T("Nachricht")),
   Field("commentdate", "datetime", default=request.now),
   Field("senderip", "string", default=request.env['http_host']))

db.plugin_feedbacks_feedback.commentdate.writable=False
db.plugin_feedbacks_feedback.senderip.writable=False
db.plugin_feedbacks_feedback.feeling.requires = IS_IN_SET({'happy':T('gefällt mir'),'unhappy':T('gefällt mir nicht')}, error_message=T("Bitte eine Emotion wählen"))
db.plugin_feedbacks_feedback.message.requires = IS_LENGTH(140,1, error_message=T("Bitte eine Nachricht zwischen 1 und 140 Zeichen eingeben."))
db.plugin_feedbacks_feedback.feeling.widget = SQLFORM.widgets.radio.widget
db.plugin_feedbacks_feedback.feeling.widget = lambda field,value: \
    SQLFORM.widgets.radio.widget(field,value, style='divs')


def plugin_feedbacks():
    from gluon.tools import PluginManager
    plugins = PluginManager('feedbacks', feeling_label='Your feedback')

    feedback = db.plugin_feedbacks_feedback
    #feedback.label=plugins.feedbacks.feedback_label

    return LOAD('plugin_feedbacks','feedback.load',ajax=True)