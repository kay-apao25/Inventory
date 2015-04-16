import  json
from dosql import doSql

class Supplier(object):
    
    """Supplier Class"""

    def add_supplier(supplier_num, supplier_name, supplier_address, telephone_number, \
    	credit_limit, debit_amt, credit_amt, balance_amt, contact_person, remarks):

        """Function for adding supplier"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_supplier", supplier_num, supplier_name,\
         supplier_address, telephone_number, credit_limit, debit_amt, credit_amt, balance_amt, \
         contact_person, remarks), True)

        return json.dumps(res.parse_result(ans))