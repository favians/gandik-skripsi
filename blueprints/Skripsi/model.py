from blueprints import db
from flask_restful import fields


class Skripsi(db.Model):
    __tablename__ = "skripsi"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    sistole = db.Column(db.Integer, nullable=False)
    diastole = db.Column(db.Integer, nullable=False)

    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'nama': fields.String,
        'sistole': fields.String,
        'diastole': fields.Integer,
    }

    response_field_with_client = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'nama': fields.String,
        'sistole': fields.String,
        'diastole': fields.Integer,
    }

    response_field_organisasi = {
        'page': fields.Integer,
        'total_page': fields.Integer,
        'per_page': fields.Integer    
    }

    def __init__(self, created_at, nama, sistole, diastole):
        self.created_at = created_at
        self.nama = nama
        self.sistole = sistole
        self.diastole = diastole

    def __repr__(self):
        return '<Pets %r>' % self.id