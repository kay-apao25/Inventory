import  json
from dosql import doSql

class Customer(object):
    
    """Customer Class"""

    def add_customer(dce, name, cost_center_no, credit_limit, debit_amt, credit_amt, balance_amt):

        """Function for adding Customer"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_customer", dce, name, cost_center_no, \
        	credit_limit, debit_amt, credit_amt, balance_amt), True)

        return json.dumps(res.parse_result(ans))