from flask import render_template, request, Blueprint, redirect, url_for, session, flash
from companyblog.models import BlogPost, Contact
from companyblog.users.forms import ContactForm
from companyblog import db

core = Blueprint('core', __name__)


@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', blog_posts=blog_posts)


@core.route('/info', methods=['GET', 'POST'])
def info():
    form = ContactForm()
    if form.validate_on_submit():
        try:

            session['email'] = form.email.data
            session['subject'] = form.subject.data
            session['message'] = form.message.data

            message = Contact(email=form.email.data,
                              subject=form.subject.data,
                              message=form.message.data)

            db.session.add(message)
            db.session.commit()
            return redirect(url_for('core.thankyou'))
        except:
            return ('did not sve to database')

    return render_template('info.html', form=form)


@core.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
