from flask import Blueprint, render_template, abort
from models.blog_model import BlogPost, BlogCategory, BlogTag

blog = Blueprint('blog', __name__)

@blog.route('/blog')
def index():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category')
    tag_slug = request.args.get('tag')
    search = request.args.get('q')
    
    query = BlogPost.query.filter_by(status='published')
    
    if category_slug:
        category = BlogCategory.query.filter_by(slug=category_slug).first_or_404()
        query = query.join(BlogPost.categories).filter(BlogCategory.id == category.id)
    
    if tag_slug:
        tag = BlogTag.query.filter_by(slug=tag_slug).first_or_404()
        query = query.join(BlogPost.tags).filter(BlogTag.id == tag.id)
    
    if search:
        query = query.filter(
            db.or_(
                BlogPost.title.ilike(f'%{search}%'),
                BlogPost.content.ilike(f'%{search}%')
            )
        )
    
    posts = query.order_by(BlogPost.published_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    
    categories = BlogCategory.query.all()
    tags = BlogTag.query.all()
    featured_posts = BlogPost.query.filter_by(
        status='published', is_featured=True
    ).order_by(BlogPost.published_at.desc()).limit(3).all()
    
    return render_template('blog.html',
                         posts=posts,
                         categories=categories,
                         tags=tags,
                         featured_posts=featured_posts,
                         current_category=category_slug,
                         current_tag=tag_slug,
                         search=search)

@blog.route('/blog/<string:slug>')
def post(slug):
    post = BlogPost.query.filter_by(slug=slug, status='published').first_or_404()
    post.increment_views()
    
    # Get related posts
    related_posts = BlogPost.query.filter(
        BlogPost.id != post.id,
        BlogPost.status == 'published'
    ).join(BlogPost.categories).filter(
        BlogCategory.id.in_([c.id for c in post.categories])
    ).order_by(BlogPost.published_at.desc()).limit(3).all()
    
    return render_template('blog_post.html', post=post, related_posts=related_posts)

from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user
from slugify import slugify
from app import db
import os

@blog.route('/admin/blog/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if not current_user.is_admin:
        abort(403)
    
    if request.method == 'POST':
        post = BlogPost(
            title=request.form.get('title'),
            content=request.form.get('content'),
            excerpt=request.form.get('excerpt'),
            seo_title=request.form.get('seo_title'),
            seo_description=request.form.get('seo_description'),
            seo_keywords=request.form.get('seo_keywords'),
            status=request.form.get('status', 'draft'),
            is_featured=bool(request.form.get('is_featured')),
            author_id=current_user.id
        )
        
        post.slug = post.generate_slug()
        
        if post.status == 'published' and not post.published_at:
            post.published_at = datetime.utcnow()
        
        # Handle featured image
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file.filename:
                filename = f"blog_{post.slug}_{file.filename}"
                file.save(os.path.join('static', 'images', 'blog', filename))
                post.featured_image = f"images/blog/{filename}"
        
        # Handle categories
        category_ids = request.form.getlist('categories')
        for cat_id in category_ids:
            category = BlogCategory.query.get(cat_id)
            if category:
                post.categories.append(category)
        
        # Handle tags
        tag_names = request.form.get('tags', '').split(',')
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                tag = BlogTag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = BlogTag(
                        name=tag_name,
                        slug=slugify(tag_name)
                    )
                    db.session.add(tag)
                post.tags.append(tag)
        
        db.session.add(post)
        db.session.commit()
        
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    categories = BlogCategory.query.all()
    return render_template('admin/blog_form.html', categories=categories, post=None)

from datetime import datetime
