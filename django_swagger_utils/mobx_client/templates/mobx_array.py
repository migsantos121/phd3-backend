array="""{% autoescape off %}
/*
 * @author: Tanmay B
 * @flow
 */
import { observable } from 'mobx'
{{import_str}}
import type { IObservableArray } from 'mobx'
class {{filename}}{
    @observable orders: IObservableArray<{{classname}}>
    constructor() {
        this.orders = observable([])
    }
}

const {{objectname}} = new {{filename}}()
export default {{objectname}}
{% endautoescape %}
"""

"""


{'import_str':'',
'filename':'',
'classname':'',
'objectname':''
}
"""
