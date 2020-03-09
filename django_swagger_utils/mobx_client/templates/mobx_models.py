models = """{% autoescape off %}
/*
 * @author: Tanmay B
 * @flow
 */
{% if extra_imports|length > 0 %}{{extra_imports}}{%endif%}
{% if import_flag %}import type { IObservableArray } from 'mobx';{%endif%}
import { observable, action } from "mobx";
{% if api_type_import|length > 0 %}import type { {{api_type_import}} } from "./type.js";{%endif%}
class {{model_name}}{
    {% for each_field,type in fields %}@observable {{each_field}}:{{type}};{% if not forloop.last %}
    {% endif %}{% endfor %}
        
    constructor({{camel_name}}:API{{model_name}} = {}){
        {% for each_field,right_side,default in constructor %}this.{{each_field}}={% if 'new ' not in right_side %}{{camel_name}}.{% endif %}{{right_side}}{{default}};
        {% endfor %}
    }
    
    @action.bound getRequestData(){
        return {
            {% for r_field,r_type in request_data %}{{r_field}}:this.{{r_field}}{% if r_type == 'object' %}.getRequestData(){% endif %},
            {% endfor %}
        }
    }
    
    {% for name,each_field,type1,default_symbol,new_field in actions %}@action.bound set{{name}}({{each_field}}{{type1}}{{default_symbol}}){
        this.{{each_field}}={{new_field}};
    }
    {% if not forloop.last %}
    {% endif %}{% endfor %}
}
export default {{model_name}};
{% endautoescape %}
"""



# modelname is BasicOrder
# each_field is orderTotal
# integer is type , OrderStatus is also type
# smallmodelname is basicorder
# ea
