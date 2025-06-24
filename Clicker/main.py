from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

# Создаем таблицы при запуске приложения
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
