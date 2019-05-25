from app.post.forms import SearchForm
from app import db
from app.models import Posts
from flask import (
    Blueprint,
    g,
    render_template,
    session,
)

post = Blueprint('post', __name__)

@post.before_app_request
def before_request():
    g.search_form = SearchForm()

@post.route('/posts', defaults={'id': None})
@post.route('/posts/<int:id>')
@post.route('/posts/index', defaults={'id': None})
@post.route('/posts/index/<int:id>')
def index(id):
    if id is None:
        posts_query = Posts.query
    else:
        posts_query = Posts.query.filter_by(id=id)
    if g.search_form.validate():
        q = g.search_form.q.data
        q = str(q).replace("", "or")
        posts_query = Posts.query.search(q)
    posts_items = posts_query.order_by(Posts.title.desc())
    return render_template('posts/index.html',
                            title='posts',
                            posts=posts_items
                            )