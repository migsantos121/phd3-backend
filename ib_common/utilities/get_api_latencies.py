__author__ = 'kapeed2091'


def get_api_latencies(filename):
    from django_swagger_utils.models import Latency
    from django.db.models import Avg, Max, Min

    queries = Latency.objects.values_list('operation_id').annotate(x=Max('response_time')).annotate(
        y=Min('response_time')).annotate(z=Avg('response_time')).annotate(a=Max('db_queries_count')).annotate(
        b=Min('db_queries_count')).annotate(c=Avg('db_queries_count')).annotate(max_db_time=Max('db_time')).annotate(
        min_db_time=Min('db_time')).annotate(avg_db_time=Avg('db_time'))

    f = open(filename, 'w')
    f.write(
        'operation_id, max_response_time, min_response_time, avg_response_time, max_db_queries, min_db_queries,' +
        ' avg_db_queries, max_db_time, min_db_time, avg_db_time\n')
    for query in queries:
        print query
        operation_id = query[0]
        max_response_time = query[1]
        min_response_time = query[2]
        avg_response_time = query[3]
        max_db_queries = query[4]
        min_db_queries = query[5]
        avg_db_queries = query[6]
        max_db_time = query[7]
        min_db_time = query[8]
        avg_db_time = query[9]

        print operation_id, max_response_time, min_response_time, avg_response_time, max_db_queries, min_db_queries, avg_db_queries, max_db_time, min_db_time, avg_db_time

        f.write(str(operation_id) + ',' + str(max_response_time) + ',' + str(min_response_time) + ',' + str(
            avg_response_time) + ',' + str(max_db_queries) + ',' + str(min_db_queries) + ',' + str(
            avg_db_queries) + ',' + str(max_db_time) + ',' + str(min_db_time) + ',' + str(avg_db_time) + '\n')
    f.close()
    return
