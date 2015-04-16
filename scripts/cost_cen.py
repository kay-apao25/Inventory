import  json
from dosql import doSql

class Cost_Cen(object):
    
    """Cost Center Class"""

    def add_cost_center (cost_center_name, functional_group):

        """Function for adding Cost Center Station"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_cost_cent", cost_center_name, \
            functional_group), True)

        return json.dumps(res.parse_result(ans))