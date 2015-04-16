create table product(
	asset_code serial primary key,
	nsn char, 
  slc_num int, 
  inv_station_no_fk char references inventory_stat(inv_station_no),
  cost_center_no_fk int references cost_cent(cost_center_no), 
  item_name text,
  generic_name text,
  brand text,
  part_num char,
  manufacture_date date,
  expiry_date date,
  class char,
  stock char,
  block char,
  unit_measure char,
  unit_cost numeric,
  quantity numeric,
  average_amt numeric,
  status char,
  balance_limit numeric,
  serial_number char,
  model text,
  amount numeric,
  description text,
  remark text
  --constraint product_pk primary key (asset_code, cost_center_no_fk)
);

-- HOW TO USE:
-- SELECT add_prodprof('computer', 'Iligan City', 'Keira Montiel', '38429349394', 'Intel Motherboard Black, DH 61 WWB3', 3, 1326.88, ....);
create or replace function add_prodprof(p_nsn char, p_slc_num int, p_inv_station_no_fk char, p_cost_center_no_fk int, p_generic_name text,
  p_brand text, p_part_num char, p_manufacture_date date, p_expiry_date date, p_class char, p_stock char, p_block char, p_unit_measure char,
  p_unit_cost numeric, p_quantity numeric, p_average_amt numeric, p_status char, p_balance_limit numeric, p_item_name text, p_serial_number char,
  p_model text, p_remark text, p_description text,	p_amount numeric)
    return text as
$$
  declare
    v_asset_code int;
    v_cost_center_no int;
  begin
    select asset_code, cost_center_no_fk from product into v_asset_code, v_cost_center_no
  		where asset_code = p_asset_code and cost_center_no_fk = p_cost_center_no_fk;

     if v_asset_code isnull and v_cost_center_no isnull then
      insert into product(nsn, slc_num, inv_station_no_fk, cost_center_no_fk, generic_name, brand, part_num, manufacture_date, 
            expiry_date, class, stock, block, unit_measure, unit_cost, quantity, average_amt, status, balance_limit, 
            item_name, serial_number, model, remark, description, amount)
      		values (p_nsn, p_slc_num, p_inv_station_no_fk, p_cost_center_no_fk, p_generic_name, p_brand, p_part_num, p_manufacture_date, 
            p_expiry_date, p_class, p_stock, p_block, p_unit_measure, p_unit_cost, p_quantity, p_average_amt, p_status, p_balance_limit, 
            p_item_name, p_serial_number, p_model, p_remark, p_description,  p_amount);
      return 'Successfully added';
    else
      update product
      
      set item_name = p_item_name, amount = p_amount, nsn = p_nsn, slc_num = p_slc_num, inv_station_no = p_inv_station_no_fk, 
        cost_center_no_fk = p_cost_center_no_fk, generic_name = p_generic_name, brand = p_brand, part_num = p_part_num, 
        manufacture_date = p_manufacture_date, expiry_date = p_expiry_date, class = p_class, stock = p_stock, block = p_block, 
        unit_measure = p_unit_measure, unit_cost = p_unit_cost, quantity = p_quantity, average_amt = p_average_amt,
        status = p_status, balance_limit = p_balance_limit, serial_number = p_serial_number, remark = p_remark,
        description = p_description, 
        where asset_code = v_asset_code and cost_center_no_fk = v_cost_center_no;
      
      return 'Successfully updated';
    end if;
  end;
$$
	language 'plpgsql';
