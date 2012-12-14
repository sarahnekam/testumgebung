from gluon.tools import prettydate
import datetime

session.plugin_feedbacks = {"sentFeedback": 0, "time":request.now}

@auth.requires_login()
def feedback():
    feedback = db.plugin_feedbacks_feedback
    form = SQLFORM(feedback)
    

    show_tab = ''
    if form.process(onvalidation=check_plugin_feedbacks_feedback_form).accepted:
        response.flash = T("Vielen Dank für Ihr Feedback.")
        session.plugin_feedbacks["sentFeedback"] = 1
        session.plugin_feedbacks["time"] = request.now
        if form.vars.feeling == "happy":
            show_tab = 'happy'
        else:
            show_tab = 'unhappy'
        
    likes = db(db.plugin_feedbacks_feedback.feeling == "happy").select(orderby=~db.plugin_feedbacks_feedback.commentdate)
    dislikes = db(db.plugin_feedbacks_feedback.feeling == "unhappy").select(orderby=~db.plugin_feedbacks_feedback.commentdate)
    
    for likerow in likes:
        likerow.commentdate = prettydate(likerow.commentdate,T)
    for dislikerow in dislikes:
        dislikerow.commentdate = prettydate(dislikerow.commentdate,T)
    
    test = datetime.datetime.now() - datetime.timedelta(minutes=15)
    records = db((db.plugin_feedbacks_feedback.senderip == form.vars.senderip) & (db.plugin_feedbacks_feedback.commentdate > test)).select()
    
    
    return dict(form=form, likes=likes, dislikes=dislikes, show_tab=show_tab)

def check_plugin_feedbacks_feedback_form(form):
    """
    pruefen, dass eine IP nicht so oft hintereinander Feedback sendet
    """
    # todo: auf 30 Minuten setzen, datetime irgendwie als String formatieren
    #records = db((db.plugin_feedbacks_feedback.senderip == form.vars.senderip) & (db.plugin_feedbacks_feedback.commentdate > str(datetime.datetime.now() - datetime.timedelta(minutes=15)))).select()
    
    
    
    if session.plugin_feedbacks["sentFeedback"] == 1 and session.plugin_feedbacks["time"] > (datetime.datetime.now() - datetime.timedelta(minutes=15)):
        form.errors.message = T('Wir freuen uns, dass Sie uns Feedback geben möchten. Aus Sicherheitsgründen kann von einer Person nur einmal pro halbe Stunde ein Feedback gegeben werden.')