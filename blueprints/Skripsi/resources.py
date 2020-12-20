import datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

from .model import Skripsi

from blueprints import db, app
from sqlalchemy import desc

bp_skripsi = Blueprint("skripsi", __name__)
api = Api(bp_skripsi)


class SkripsiResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',location='args', help='invalid id', required=True)
        args = parser.parse_args()

        qry = Skripsi.query.get(args["id"])

        if qry is not None:
            return {"status":"success", "result":marshal(qry, Skripsi.response_field)}, 200, {'Content-Type':'application/json'}

        return {'status':'failed',"result":"ID Not Found"}, 404, {'Content-Type':'application/json'}


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name",location="json", help="invalid name", required=True)
        parser.add_argument("sistole",location="json", help="invalid sistole", required=True)
        parser.add_argument("diastole",location="json", help="invalid diastole", required=True)
        args = parser.parse_args()
        
        qry = Skripsi(datetime.datetime.now(), args["name"], args["sistole"], args["diastole"])
 
        db.session.add(qry)
        db.session.commit()

        app.logger.debug("DEBUG : %s ", qry)

        return {"status":"success", "result":marshal(qry, Skripsi.response_field)}, 200, {"Content-Type":"application/json"}

class SkripsiResourceList(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("p", type=int, location="args", default=1)
        parser.add_argument("rp",type=int, location="args", default=25)
        parser.add_argument("name",location="args", help="invalid isbn")
        args =parser.parse_args()

        offset = (args["p"] * args["rp"]) - args["rp"]

        qry = Skripsi.query

        if args["name"] is not None:
            qry = qry.filter_by(name=args["name"])

        result = []
        for row in qry.limit(args["rp"]).offset(offset).all():
            result.append(marshal(row, Skripsi.response_field))
        
        results = {}
        results["page"] = args["p"]
        results["total_page"] = len(result) // args["rp"] +1
        results["per_page"] = args["rp"]
        results["data"] = result
        
        return {"status":"success", "result":results}, 200, {"Content-Type":"application/json"}



api.add_resource(SkripsiResource, "","")
api.add_resource(SkripsiResourceList, "/list")

