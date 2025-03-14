from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Thay bằng key bảo mật của bạn
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # Sử dụng SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Model User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    followed_posts = db.relationship('PostFollow', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Model Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    followers = db.relationship('PostFollow', backref='post', lazy='dynamic')

# Model Comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

# Model PostFollow (dành cho theo dõi bài viết)
class PostFollow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post'),)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and not user.is_blocked:
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email hoặc mật khẩu không đúng, hoặc tài khoản bị khóa.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('Email hoặc username đã tồn tại!', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        if 'submit_post' in request.form:
            title = request.form.get('title')
            content = request.form.get('content')
            response = requests.get('https://picsum.photos/300/200')
            image_url = response.url if response.status_code == 200 else None
            post = Post(title=title, content=content, image_url=image_url, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Bài viết đã được đăng thành công!', 'success')
            return redirect(url_for('dashboard'))
        elif 'submit_comment' in request.form:
            post_id = request.form.get('post_id')
            content = request.form.get('comment_content')
            if content and post_id:
                comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
                db.session.add(comment)
                db.session.commit()
                flash('Bình luận đã được gửi!', 'success')
            return redirect(url_for('dashboard'))
        elif 'follow_post' in request.form:
            post_id = request.form.get('post_id')
            post = Post.query.get(post_id)
            if post and post.user_id != current_user.id and not current_user.followed_posts.filter_by(post_id=post_id).first():
                post_follow = PostFollow(user_id=current_user.id, post_id=post_id)
                db.session.add(post_follow)
                db.session.commit()
                flash('Đã theo dõi bài viết!', 'success')
            return redirect(url_for('dashboard'))
        elif 'unfollow_post' in request.form:
            post_id = request.form.get('post_id')
            post_follow = PostFollow.query.filter_by(user_id=current_user.id, post_id=post_id).first()
            if post_follow:
                db.session.delete(post_follow)
                db.session.commit()
                flash('Đã hủy theo dõi bài viết!', 'success')
            return redirect(url_for('dashboard'))

    page = request.args.get('page', 1, type=int)
    per_page = 5
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=per_page)
    return render_template('dashboard.html', user=current_user, posts=posts.items, pagination=posts, total_posts=posts.total)

@app.route('/toggle_follow/<int:post_id>', methods=['POST'])
@login_required
def toggle_follow(post_id):
    post = Post.query.get_or_404(post_id)
    existing_follow = PostFollow.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    if existing_follow:
        db.session.delete(existing_follow)
        flash(f'Đã bỏ theo dõi bài viết "{post.title}".', 'info')
    else:
        if post.user_id != current_user.id:
            new_follow = PostFollow(user_id=current_user.id, post_id=post.id)
            db.session.add(new_follow)
            flash(f'Bạn đã theo dõi bài viết "{post.title}".', 'success')
        else:
            flash('Bạn không thể theo dõi bài viết của chính mình.', 'warning')

    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/admin/toggle_block/<int:user_id>')
@login_required
def toggle_block(user_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền thực hiện hành động này.', 'danger')
        return redirect(url_for('dashboard'))
    user = User.query.get_or_404(user_id)
    user.is_blocked = not user.is_blocked
    db.session.commit()
    flash(f'Đã {"khóa" if user.is_blocked else "mở khóa"} tài khoản {user.username}.', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            user = User(username='user', email='user@example.com')
            user.set_password('user123')
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)