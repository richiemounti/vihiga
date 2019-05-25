from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for
)
from app.admin.forms import PostItemForm
from app.models import Posts
from app import db
from flask_login import login_required

admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
def require_login():
    pass

@admin.route('/admin')
@admin.route('/admin/index')
def index():
    post_items = Posts.query.all()
    return render_template('admin/index.html',
                            post_items=post_items,
                            title="Posts"
                            )

@admin.route('/admin/new', methods=['GET', 'POST'])
def new():
    form = PostItemForm()
    if form.validate_on_submit():
        post_item = Posts()
        form.populate_obj(post_item)
        db.session.add(post_item)
        db.session.commit()
        flash('Post added!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/new.html',
                            form=form,
                            title="Posts"
                            )

@admin.route('/admin/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    post_item = Posts.query.filter_by(id=id).first_or_404()
    form = PostItemForm(obj=post_item)
    if form.validate_on_submit():
        form.populate_obj(post_item)
        db.session.add(post_item)
        db.session.commit()
        flash('Post is updated!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/edit.html',
                            post_item=post_item,
                            form=form,
                            title='Posts'
                            )

@admin.route('/admin/details/<id>')
def details(id):
    post_item = Posts.query.filter_by(id=id).first_or_404()

    return render_template('admin/details.html',
                            post_item=post_item,
                            title='Posts'
                            )