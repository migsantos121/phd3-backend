apimodel="""
{% autoescape off %}
/*
 * @author: Tanmay B
 * @flow
 */
{% if import|length > 0 %}{{import}}{%endif%}
{% if import_flag %}import type { IObservableArray } from 'mobx';{%endif%}

export type {{class_name}}={
    {% for each_field,type in fields %}{{each_field}}:{{type}}{% if not forloop.last %},
    {% endif %}{% endfor %}
};
{% endautoescape %}
"""
