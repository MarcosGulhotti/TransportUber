from app.configs.database import db

cargas_categorias = db.Table('cargas_categorias',
  db.Column('id', db.Integer, primary_key=True),
  db.Column('categoria_id', db.Integer, db.ForeignKey('categorias.id')),
  db.Column('carga_id', db.Integer, db.ForeignKey('cargas.id')),
)
