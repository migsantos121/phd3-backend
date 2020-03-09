# coding=utf-8
import json
import logging

logger = logging.getLogger(__name__)


def get_db_time(queries):
    total_time = 0
    queries_data = {}
    duplicate_queries = 0
    for query in queries:
        query_time = query.get('time')
        if query_time is None:
            # django-debug-toolbar monkeypatches the connection
            # cursor wrapper and adds extra information in each
            # item in connection.queries. The query time is stored
            # under the key "duration" rather than "time" and is
            # in milliseconds, not seconds.
            query_time = query.get('duration', 0) / 1000
        total_time += float(query_time)
        if query["sql"] not in queries_data:
            queries_data[query["sql"]] = {"count": 1, "time": float(query_time)}
        else:
            if queries_data[query["sql"]]["count"] == 1:
                duplicate_queries += 1
            queries_data[query["sql"]]["count"] += 1
            queries_data[query["sql"]]["time"] += float(query_time)

    queries_data = json.dumps(queries_data)
    return total_time, duplicate_queries, queries_data


def response_time(app_name, operation_id):
    """

    :return:
    """

    def decorator(function):
        """

        :param function:
        :return:
        """

        def handler(*args, **kwargs):
            from time import time
            start_time = time()
            from django.db import connection
            return_value = function(*args, **kwargs)
            end_queries = connection.queries
            db_queries_count = len(end_queries)
            db_time, duplicate_queries, db_queries = get_db_time(end_queries)
            end_time = time()
            total_time = end_time - start_time
            print ("App Name: %s" % app_name)
            print ("Operation Id: %s" % operation_id)
            print ("Endpoint Response Time: %s" % total_time)
            print ("Total DB Queries: %d " % db_queries_count)
            from django_swagger_utils.models import Latency
            Latency.objects.create(
                app_name=app_name,
                operation_id=operation_id,
                response_time=total_time,
                db_queries_count=db_queries_count,
                db_queries=db_queries,
                db_time=db_time,
                duplicate_queries=duplicate_queries,
            )
            return return_value

        handler.__doc__ = function.__doc__
        return handler

    return decorator
