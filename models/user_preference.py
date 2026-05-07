from startup.extensions import db

class UserPreference(db.Model):
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    display_name = db.Column(db.String(64))
    email = db.Column(db.String(32))
    country = db.Column(db.String(64))

    user = db.relationship("User", back_populates="preferences")