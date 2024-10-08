from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///board.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    action = request.args.get('action', None)
    post_id = request.args.get('id', None)

    if action == "new" and request.method == "POST":
        # 새 글 작성 처리
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

    elif action == "edit" and post_id and request.method == "POST":
        # 게시글 수정 처리
        post = Post.query.get(post_id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/')

    elif action == "edit" and post_id:
        # 게시글 수정 페이지
        post = Post.query.get(post_id)
        return render_template('index.html', action="edit", post=post)

    elif action == "view" and post_id:
        # 게시글 상세보기 페이지
        post = Post.query.get(post_id)
        return render_template('index.html', action="view", post=post)

    else:
        # 기본: 게시글 목록
        posts = Post.query.all()
        return render_template('index.html', action=None, posts=posts)

@app.route('/delete/<int:id>')
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
