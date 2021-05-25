from flask import Response
import json, datetime
import datetime


class TunerAPI:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_orders(self, id):
        query = f"SELECT channel_id, start, end FROM record_orders \
            WHERE tuner_id = {id}"

        ts = datetime.datetime.now().timestamp()
        try:
            orders = self.db_manager.execute_query(query)
        except Exception as exc:
            return Response(str(exc), status=500)

        result = [
            {"channel_id": str(o[0]), "start": o[1], "end": o[2]}
            for o in orders
            if o[1] > ts
        ]

        return Response(json.dumps(result), status=200)