from app import db
from datetime import datetime
from slugify import slugify

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    featured_image = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # SEO Fields
    seo_title = db.Column(db.String(70))
    seo_description = db.Column(db.String(160))
    seo_keywords = db.Column(db.String(500))
    canonical_url = db.Column(db.String(500))
    
    # Publishing
    status = db.Column(db.String(50), default='draft')  # draft, published, archived
    published_at = db.Column(db.DateTime)
    is_featured = db.Column(db.Boolean, default=False)
    views_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='blog_posts')
    categories = db.relationship('BlogCategory', secondary='post_categories', backref='posts')
    tags = db.relationship('BlogTag', secondary='post_tags', backref='posts')
    
    def generate_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while BlogPost.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    
    def get_reading_time(self):
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))  # Assuming 200 words per minute
    
    def increment_views(self):
        self.views_count += 1
        db.session.commit()

class BlogCategory(db.Model):
    __tablename__ = 'blog_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BlogTag(db.Model):
    __tablename__ = 'blog_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Association tables
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_posts.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('blog_categories.id'), primary_key=True)
)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('blog_tags.id'), primary_key=True)
)
