URL = """{% autoescape off %}from django.conf.urls import url

{% for path_name, each_path in path_names.items %}{{ each_path.view_environment.import_str }}
{% endfor %}

urlpatterns = [{% for path_name, each_path in path_names.items %}{% for each_url_name in each_path.path_method_dict %}
    url(r'^{{ each_url_name }}$', {{ each_path.view_environment.path_name }}),{% endfor %}{% endfor %}
]
{% endautoescape %}
"""