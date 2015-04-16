import json
from dosql import doSql 

class Irr(Object):
    """class for the irr library"""

    def add_irr(self, irr_no_fk , asset_code_fk , slc_num , cost_center_no_fk , quantity_actual ,\
                 quantity_accepted , quantity_rejected , quantity_balance , date_recv ,\
                wo_no , remark):

        """Function for adding irr"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from \
            add_irr",irr_no_fk , asset_code_fk , slc_num , cost_center_no_fk , quantity_actual ,\
                 quantity_accepted , quantity_rejected , quantity_balance , date_recv ,\
                wo_no , remark ), True)

        return json.dumps(res.parse_result(ans))

    def get_irr(self, irr_no_fk):
        """function for get irr"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from \
            get_irr",irr_no_fk ), False)

        return json.dumps(res.parse_result(ans))


