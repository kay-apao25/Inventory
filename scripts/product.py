import  json
from dosql import doSql

class Product(object):

    def add_prodprof (item_name, supplier_address, supplier_name, serial_number, description, model, amount):

        res = doSql()

        ans = res.execqry(res.buildqry("select * from add_prodprof",\
         str(feel_id)), True)

        return json.dumps(res.parse_result(ans))

    
    
