create table product{
	asset_code serial int primary key,
	item_name text,
    supplier_name text,
    supplier_address text,
    serial_number char,
    quantity, bigint,
    model text,
    amount numeric,
    description text,
    constraint product_pk (serial_number, supplier_name, model)
};

-- HOW TO USE:
-- SELECT add_prodprof('computer', 'Iligan City', 'Keira Montiel', 'none', 'lala', 3, 1326.88);
create or replace function add_prodprof(p_item_name text, p_supplier_address text, p_supplier_name text, p_serial_number char, 
																		p_description text,	p_model text, p_quantity bigint, p_amount numeric)
    returns text as
$$
  declare
    v_supplier_name text;
    v_serial_number char;
    v_model text;
  begin
    select supplier_name, serial_number, model from product into v_supplier_name, v_serial_number, v_model
  		where supplier_name = p_supplier_name and serial_number = p_serial_number and model = p_model;

     if v_supplier_name isnull and v_serial_number isnull and v_model isnull then
      insert into product(item_name, supplier_name, supplier_address, serial_number, quantity, model, amount)
      		values (p_item_name, p_supplier_name, p_supplier_address, p_serial_number, p_quantity, p_model, p_amount);
      return 'Successfully added';
    else
      update product
      
      set item_name = p_item_name, supplier_address = p_supplier_address, quantity = p_quantity, amount = p_amount
        where supplier_name = p_supplier_name and serial_number = p_serial_number and model = p_model;
      
      return 'Successfully updated';
    end if;
  end;
$$
	language 'plpgsql';