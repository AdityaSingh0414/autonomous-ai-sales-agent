
# Database Base aur engine import karna.
from backend.database.connection import Base, engine

# Database models import karna.
from backend.database.models import Lead, Appointment


# Database mein defined tables create karna.
Base.metadata.create_all(bind=engine)


# Success message print karna.
print("Database tables created successfully!")
