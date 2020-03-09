"""
Created on 11/07/17

@author: revanth
"""


def execution_time(function_name=''):
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
            return_value = function(*args, **kwargs)
            end_time = time()
            total_time = end_time - start_time
            if function_name is None or function_name == '':
                print ("Execution Time: %s, %s" % (function.__name__, total_time))
            else:
                print ("Execution Time: %s, %s" % (function_name, total_time))
            return return_value

        handler.__doc__ = function.__doc__
        return handler

    return decorator
