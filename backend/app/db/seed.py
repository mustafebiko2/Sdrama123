import os

from app.auth.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.shared.models import Category, Genre, Role, Setting, User


def get_or_create(db, model, defaults=None, **filters):
    record = db.query(model).filter_by(**filters).first()
    if record:
        return record
    record = model(**filters, **(defaults or {}))
    db.add(record)
    return record


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin_role = get_or_create(db, Role, name="admin")
        get_or_create(db, Role, name="user")

        admin_email = os.getenv("ADMIN_EMAIL", "admin@sdrama123.local")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin12345")
        admin = db.query(User).filter(User.email == admin_email).first()
        if admin is None:
            admin = User(
                name="Sdrama123 Admin",
                email=admin_email,
                hashed_password=hash_password(admin_password),
                roles=[admin_role],
            )
            db.add(admin)

        for name, slug in [("Drama", "drama"), ("Action", "action"), ("Series", "series"), ("Movies", "movies")]:
            get_or_create(db, Genre, name=name, slug=slug)
            get_or_create(db, Category, name=name, slug=slug)

        get_or_create(db, Setting, key="website_name", defaults={"value": "Sdrama123"})
        get_or_create(db, Setting, key="default_language", defaults={"value": "English"})

        db.commit()
        print(f"Seed complete. Admin login: {admin_email} / {admin_password}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
