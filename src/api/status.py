from flask import Response
import json
from src.database.db_model import JsonConverter, TunerStatus


class StatusAPI:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def post_status(self, id, status):
        query = f"""INSERT OR REPLACE INTO tuner_status(tuner_id, free_space, is_recording, current_recording_time, current_recording_size)
            VALUES(?, ?, ?, ?, ?)"""
        args = [
            id,
            status.free_space,
            status.is_recording,
            status.current_recording_time,
            status.current_recording_size,
        ]

        if self.db_manager.run_query(query, args, return_result=False):
            return Response("Successfully posted status", status=201)
        else:
            return Response("Something went wrong", status=500)

    def get_status(self, id):
        query = f"""SELECT free_space, is_recording, current_recording_size, current_recording_time 
            FROM tuner_status
            WHERE tuner_id = ?"""
        args = [id]

        result = self.db_manager.run_query(query, args)
        if result:
            tuner_status = TunerStatus(*result[0])
            return Response(
                json.dumps(tuner_status, default=lambda o: o.__dict__, indent=4),
                mimetype="json",
                status=200,
            )
        else:
            return Response("Something went wrong", status=500)
