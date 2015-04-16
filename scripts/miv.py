import json
from dosql import doSql 

class Miv(Object):
    """class for the miv library"""

    def add_irr(self, irr_no, inv_station_no, asset_code, dce_custodian , dce_user, cost_center_no, wrs_num,\
                    quantity, amount , date_issued , doc_date, remark):

        """Function for adding miv"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from \
            add_miv",irr_no, inv_station_no, asset_code, dce_custodian , dce_user, cost_center_no, wrs_num,
                    quantity, amount , date_issued , doc_date, remark ), True)

        return json.dumps(res.parse_result(ans))

    def get_miv(self, miv_no):
        """function for get miv"""

        res = doSql()

        ans = res.execqry(res.buildqry("select * from \
            get_miv",miv_no ), False)

        return json.dumps(res.parse_result(ans))
