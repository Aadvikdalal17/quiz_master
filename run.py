def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if admin user exists, if not create one
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin_password')
            db.session.add(admin)
            db.session.commit()
            
        print("Database tables created successfully!")