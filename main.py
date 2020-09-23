from app import app
from app import db


def main():
    # Create DB
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
