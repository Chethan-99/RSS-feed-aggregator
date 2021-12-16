import re
from flask import Blueprint, render_template,redirect,request
from flask.helpers import flash
from .models import db

from .models import Link

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html') 


@views.route('/add_link', methods=['POST'])
def add_link():
    original_url = request.form['original_url']
    short_url = request.form['short_url']
    link = Link(original_url=original_url, short_url=short_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html', 
        new_link=link.short_url, original_url=link.original_url)


@views.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.original_url) 

@views.route('/stats')
def stats():
    links = Link.query.all()
    return render_template('stats.html',links=links)


@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/add', methods = ['GET','POST'])
def add():
    message = ''
    if request.method == 'POST':
        full_url = request.form.getlist('field[]')
        n = request.form['limit']
        i = 1
        str = 'http://127.0.0.1:8000/rss?f='
        
        for value in full_url:
            if value != '':
                if i == 1:
                    str += value 
                    i += 1
                else:
                    str +='&f=' + value
                    i += 1
        if n:
            str += '&n=' + n
        print(str)
        link = Link(original_url=str)
        db.session.add(link)
        db.session.commit()
        result = Link.query.filter_by(original_url=str).first_or_404()
        print(result)
        return render_template('link_added.html', new_link=result.short_url, original_url=link.original_url)
        flash('Note added', category='success')
    return render_template('url_add.html')