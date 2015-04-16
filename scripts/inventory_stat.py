import json
from dosql import doSql 

class Inventory_stat(Object):
    """class for the inventory station library"""

    def add_irr(self, inv_station_no, station_description, cost_center_no_fk):

        """Function for adding inventory station"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_miv",inv_station_no, station_description, cost_center_no_fk ), True)

        return json.dumps(res.parse_result(ans))