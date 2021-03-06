# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, redirect, flash
from apps.forms import ArticleForm, CommentForm, JoinForm
from apps import app, db
from sqlalchemy import desc
from apps.models import Article, Comment, User
from werkzeug.security import generate_password_hash


@app.route('/', methods=['GET'])
def article_list():
    context = {}
    context['article_list'] = Article.query.order_by(desc(Article.data_created)).all()
    return render_template("home.html", context=context, active_tab="timeline")


@app.route('/article/create/', methods=['GET', 'POST'])
# URL값을 받아서 이 함수를 실행해야 하니까, 'GET'은 항상 들어간다
def article_create():
    form = ArticleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            article = Article(
                title=form.title.data,
                author=form.author.data,
                category=form.category.data,
                content=form.content.data
            )

            db.session.add(article)
            db.session.commit()

            flash(u'게시물을 작성하였습니다.', 'success')
            return redirect(url_for('article_list'))

    return render_template('article/create.html', form=form, active_tab='article_create')


@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)
    comment = Comment.query.order_by(desc(Comment.date_created)).filter_by(article_id = article.id)
    return render_template('article/detail.html', article=article, comments=comment)


@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    form = ArticleForm(request.form, obj=article)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(article)
            db.session.commit()
        return redirect(url_for('article_detail', id=id))
    return render_template('article/update.html', form=form)


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/delete.html', article_id=id)
    elif request.method == 'POST':
        article_id = request.form['article_id']
        article = Article.query.get(article_id)
        db.session.delete(article)
        db.session.commit()

        flash(u'게시물을 삭제하였습니다.', 'success')
        return redirect(url_for('article_list'))


@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            comment = Comment(
                author=form.author.data,
                email=form.email.data,
                content=form.content.data,
                password=form.password.data,
                article_id=article_id
            )

            db.session.add(comment)
            db.session.commit()

            flash(u'댓글을 작성하였습니다', 'success')
        return redirect(url_for('article_detail', id=article_id))
    return render_template('comment/create.html', form=form)


@app.route('/comment/like/<int:comment_id>', methods=['GET'])
def comment_like(comment_id):
    mycomment = Comment.query.get(comment_id)
    mycomment.likecount += 1
    myarticle = mycomment.article_id
    db.session.commit()
    return redirect(url_for('article_detail', id = myarticle))


@app.route('/comment/deletecheck/<int:comment_id>', methods=['GET'])
def comment_deletecheck(comment_id):
    mycomment = Comment.query.get(comment_id)
    mycomment.commentcheck = 1
    myarticle = mycomment.article_id
    db.session.commit()
    return redirect(url_for('article_detail', id = myarticle))


@app.route('/comment/delete/<int:comment_id>', methods = ['GET', 'POST'])
def comment_delete(comment_id):
    if request.method == "POST":
        mycomment = Comment.query.get(comment_id)
        mypasswd = mycomment.password
        mycomment.commentcheck = 0
        inputpswd = request.form['pswd']
        myarticle = mycomment.article_id
        if mypasswd == inputpswd:
            db.session.delete(mycomment)
            db.session.commit()
            flash(u'댓글을 지웠습니다.', 'success')
            return redirect(url_for('article_detail', id = myarticle))
        else:
            flash(u'비밀번호가 틀렸습니다.')
            return redirect(url_for('article_detail', id = myarticle))

@app.route('/user/join/', methods =['GET','POST'])
def user_join():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                email = form.email.data,
                password = generate_password_hash(form.password.data),
                name = form.name.data
            )

            db.session.add(user)
            db.session.commit()

            flash(u'가입이 승인되었습니다. 비밀번호는 암호화되어 저장되어 관리자도 알 수 없습니다.', 'success')
            return redirect(url_for('article_list'))

    return render_template('user/join.html', form = form, active_tab = 'article_create')

#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500