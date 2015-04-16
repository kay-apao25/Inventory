import  json
from dosql import doSql

class IRR_Header(object):
    
    """IRR Header Class"""

    def add_irr_header(irr_headerkey, inv_station, reference, invoice_num, \
        po_num, dr_num, dce_cust, dce_user, proc_date, type_n, remark):

        """Function for adding IRR Header"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_irr_header", irr_headerkey, \
            inv_station, reference, invoice_num, po_num, dr_num, dce_cust, dce_user, \
            proc_date, type_n, remark), True)

        return json.dumps(res.parse_result(ans))

    def add_irr_header(irr_no):

        """Function for getting IRR Header"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from get_irr_header", irr_no), True)

        return json.dumps(res.parse_result(ans))