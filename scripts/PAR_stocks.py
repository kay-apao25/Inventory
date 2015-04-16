import json
from dosql import doSql

class PAR(Object):
    """class for PAR"""

    @classmethod
    def add_par(cls, dce, asset_code, par_no, amt_cost, remark):
        """Function for adding PAR"""

        res = doSql()
        query = x.buildqry("select add_par", dce, asset_code,
                            par_no, amt_cost, remark)
        rets = x.execqry(query, True)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

    @classmethod
    def get_par(cls, dce, asset_code):
        """Function for getting PAR"""
        res = doSql()
        query = x.buildqry("select get_par", dce, asset_code)
        rets = x.execqry(query, False)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

    @classmethod
    def del_par(cls, dce, asset_code):
        """Function for deleting PAR"""
        res = doSql()
        query = x.buildqry("select del_par", dce, asset_code)
        rets = x.execqry(query, True)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

class GARV(Object):
    """class for GARV"""

    @classmethod
    def add_garv(cls, dce, asset_code, garv_date, garv_no):
        """Function for adding GARV"""

        res = doSql()
        query = x.buildqry("select add_garv", dce, asset_code, garv_date, garv_no)
        rets = x.execqry(query, True)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

    @classmethod
    def get_garv(cls, dce, asset_code):
        """Function for getting GARV"""
        res = doSql()
        query = x.buildqry("select get_garv", dce, asset_code)
        rets = x.execqry(query, False)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

par = PAR()
garv = GARV()

"""Request for PAR object"""
def add_par(req, dce, asset_code, par_no, amt_cost, remark):
    """Request for adding PAR"""

    added_par = par.add_par(dce, asset_code, par_no, amt_cost, remark)
    return added_par

def get_par(req, dce, asset_code):
    """Request for getting PAR"""

    got_par = par.get_par(dce, asset_code)
    return got_par

def del_par(req, dce, asset_code):
    """Request for deleting PAR"""

    deleted_par = par.del_par(dce, asset_code)
    return deleted_par

"""Request for GARV object"""
def add_garv(req, dce, asset_code, garv_date, garv_no):
    """Request for adding GARV"""

    added_garv = garv.add_garv(dce, asset_code, garv_date, garv_no)
    return added_garv

def get_garv(req, dce, asset_code):
    """Request for getting GARV"""

    got_garv = garv.get_garv(dce, asset_code)
    return got_garv
