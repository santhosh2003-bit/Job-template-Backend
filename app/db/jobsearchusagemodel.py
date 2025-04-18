from app.server import db

class JobSearchUsage(db.Model):
    __tablename__ = 'job_search_usage'
    __table_args__ = {"schema": "ezeapply_schema"}  # Same schema as your user table

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("ezeapply_schema.users.id"), nullable=False)
    search_count = db.Column(db.Integer, nullable=False, default=0)
    last_search = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp())
