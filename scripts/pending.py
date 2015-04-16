import json
from dosql import doSql

class Pending(Object):
    """class for Pending"""

    @classmethod
    def add_pending(cls, item_name, supplier_address, supplier_name, serial_number,
                    description, model, amount):
        """Function for adding Pending"""

        res = doSql()
        query = x.buildqry("select add_pending", item_name, supplier_address,
                            supplier_name, serial_number, description, model,
                            amount)
        rets = x.execqry(query, True)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

    @classmethod
    def get_pending(cls, supplier_name, serial_number, model):
        """Function for getting Pending"""
        res = doSql()
        query = x.buildqry("select get_pending", supplier_name, serial_number, model)
        rets = x.execqry(query, False)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

    @classmethod
    def del_pending(cls, supplier_name, serial_number, model):
        """Function for deleting Pending"""
        res = doSql()
        query = x.buildqry("select del_pending", supplier_name, serial_number, model)
        rets = x.execqry(query, True)
        rets = x.parse_result(rets)
        return json.dumps({"msg": rets})

pending = Pending()

"""Request for Pending object"""
def add_pending(req, item_name, supplier_address, supplier_name, serial_number,
                description, model, amount):
    """Request for adding Pending"""

    added_pending = pending.add_pending(item_name, supplier_address, supplier_name,
                                        serial_number, description, model, amount)
    return added_pending

def get_pending(req, supplier_name, serial_number, model):
    """Request for getting Pending"""

    got_pending = pending.get_pending(supplier_name, serial_number, model)
    return got_pending

def del_pending(req, supplier_name, serial_number, model):
    """Request for deleting Pending"""

    delt_pending = pending.del_pending(supplier_name, serial_number, model)
    return delt_pending
