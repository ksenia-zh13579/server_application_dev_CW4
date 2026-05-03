from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float

# Ревизия и связи с предыдущими миграциями
revision = 'add_initial_data'
down_revision = '9d2eccf37b87'
branch_labels = None
depends_on = None

# Определение структуры таблицы для сидинга
products_table = table(
    'products',
    column('id', Integer),
    column('title', String),
    column('price', Float),
    column('count', Integer)
)

def upgrade():
    # Начальные данные для добавления в таблицу users
    initial_data = [
        {'id': 1, 'title': 'pencil', 'price': 84, 'count': 100},
        {'id': 2, 'title': 'notebook', 'price': 430, 'count': 120}
    ]
    # Вставка данных в таблицу
    op.bulk_insert(products_table, initial_data)

def downgrade():
    # Удаление начальных данных в случае отката
    op.execute("DELETE FROM products WHERE title IN ('pencil', 'notebook')")