import logging

from sqlalchemy import text

from app import app
from app import db


def test_db_connection():
    with app.app_context():
        try:
            db.session.query(text("1")).from_statement(text("SELECT 1")).all()
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")

if __name__ == '__main__':
    # print(app.url_map)
    print('ssss')
    logging.basicConfig(level=logging.DEBUG)
    test_db_connection()
    app.run(debug=True)
