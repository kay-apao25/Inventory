import  json
from dosql import doSql

class Product(object):

    """Product Class"""

    def add_prodprof (nsn, slc, inv_station, cost_center, generic_name, brand, part_num,\ 
        manuf_date, exp_date, class_no, stock, block, unit_measure, unit_cost, quantity, average_amt,\ 
        status, balance_limit, item_name, serial_number,  model, remark, description, amount):

        """Function for adding Product Profile"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_prodprof",nsn, slc, inv_station, cost_center, \
            generic_name, brand, part_num, manuf_date, exp_date, class_no, stock, block, unit_measure, \
            unit_cost, quantity, average_amt, status, balance_limit, item_name, serial_number,  model, \
            remark, description, amount), True)

        return json.dumps(res.parse_result(ans))
