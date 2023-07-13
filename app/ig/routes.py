from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from . import ig
from .forms import PostForm
from ..models import User, db, Post
from flask_login import login_required, current_user

@ig.route('/posts/create', methods=["GET","POST"])
@login_required
def createPostPage():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data

            my_post = Post(title, caption, img_url, current_user.user_id)

            db.session.add(my_post)
            print(my_post)
            db.session.commit()
            print(my_post)

            return redirect(url_for('ig.postsPage'))

    return render_template('createpost.html', form=form)

@ig.route('/posts')
def postsPage():
    posts = Post.query.all()
    print(posts)
    return render_template('index.html', posts = posts)

# DYNAMIC ROUTES

@ig.route('/posts/<post_id>')
def singlePostPage(post_id):
    # post = Post.query.filterby(post_id = post_id).first()
    post = Post.query.get(post_id)

    if post:
        return render_template('singlepost.html', post = post)
    else:
        return redirect(url_for('ig.homePage'))

# @app.route('/posts/like/<post_id>')
# @login_required
# def like_post(post_id):
#     like = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
#     if like:
#         return redirect(url_for('ig.homePage'))
#     else:
#         like = Like(current_user.id, post_id)
#         db.session.add(like)
#         db.session.commit()
#     return redirect(url_for('ig.homePage'))

@ig.route('/posts/like/<post_id>')
@login_required
def like_post2(post_id):
    post = Post.query.get(post_id)
    if post:
        current_user.liked_posts2.append()
        db.session.commit()
    return redirect(url_for('ig.homePage'))

# @app.route('/posts/unlike/<post_id>')
# @login_required
# def unlike_post(post_id):
#     like = Like.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
#     if like:
#         db.session.delete(like)
#         db.session.commit()
#     return redirect(url_for('ig.homePage'))

@ig.route('/posts/unlike/<post_id>')
@login_required
def unlike_post(post_id):
    post = Post.query.get(post_id)
    if post in current_user.liked_posts2:
        current_user.liked_posts2.remove(post)
        db.session.commit()
    return redirect(url_for('ig.homePage'))

@ig.route('/users')
def usersPage():
    users = User.query.all()
    return render_template('users.html', users=users)

@ig.route('/posts/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    current_user.followed.append(user)
    db.session.commit()
    return redirect(url_for('ig.usersPage'))

@ig.route('/posts/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = current_user.followed.filter_by(user_id=user_id).first()
    if user:
        current_user.followed.remove(user)
        db.session.commit()
    return redirect(url_for('ig.usersPage'))