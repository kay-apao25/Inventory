import json
from dosql import doSql 
from random import randint

class Miv(Object):
    """class for the miv library"""

    def add_irr(self, irr_no_fk, inv_station_no_fk, asset_code_fk, dce_custodian_fk , dce_user_fk, cost_center_no_fk,\
                    quantity, amount , date_issued , doc_date, remark):

        """Function for adding miv"""

        num = randint(100000,999999)
        wrs_num = "NO" + str(num)
        res = doSql()

        ans = res.execqry(res.buildqry("select * from \
            add_miv",irr_no_fk, inv_station_no_fk, asset_code_fk, dce_custodian_fk , dce_user_fk, cost_center_no_fk, wrs_num,
                    quantity, amount , date_issued , doc_date, remark ), True)

        return json.dumps(res.parse_result(ans))

    def get_miv(self, miv_no):
ti
        res = doSql()

        ans = res.execqry(res.buildqry("select * from \
            get_miv",miv_no ), False)

        return json.dumps(res.parse_result(ans))


class Miv_req(Object):

    def get_miv_req(req, miv_no):

        """Getting miv  Reports"""

        miv = Miv()

        return miv.get_miv(miv_no_)

    def add_miv_req(req, irr_no_fk, inv_station_no_fk, asset_code_fk, dce_custodian_fk , dce_user_fk, cost_center_no_fk, wrs_num,\
                    quantity, amount , date_issued , doc_date, remark):

        """adding miv  Reports"""

        miv = Miv()

        return miv.add_miv(irr_no_fk, inv_station_no_fk, asset_code_fk, dce_custodian_fk , dce_user_fk, cost_center_no_fk, wrs_num,\
                    quantity, amount , date_issued , doc_date, remark)