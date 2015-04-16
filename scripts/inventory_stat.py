import json
from dosql import doSql 

class Inventory_stat(Object):
    """class for the inventory station library"""

    def add_item(self, inv_station_no, station_description, cost_center_no_fk):

        """Function for adding inventory station"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_item",inv_station_no, station_description, cost_center_no_fk ), True)

        return json.dumps(res.parse_result(ans))

class Inventory_stat_req(Object):

    def add_inventory_stat_req(req, inv_station_no, station_description, cost_center_no_fk):

        """adding miv  Reports"""

        inventory_stat = Inventory_stat()

        return inventory_stat.add_item(inv_station_no, station_description, cost_center_no_fk)