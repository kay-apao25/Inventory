create table pending(
	asset_code serial primary key,
	item_name text,
  supplier_num_FK text,
  serial_number char,
  model text,
  amount numeric,
  description text
);

-- HOW TO USE:
-- SELECT add_pending('computer', 'Iligan City', 'Keira Montiel', 'none', 'lala', 3, 1326.88);
create or replace 
  function add_pending(p_item_name text, p_supplier_address text, p_supplier_name text, p_serial_number char, 
																		p_description text,	p_model text, p_amount numeric)
    returns text as
$$
  declare
    v_supplier_name text;
    v_serial_number char;
    v_model text;
  begin
    select supplier_name, serial_number, model from pending into v_supplier_name, v_serial_number, v_model
  		where supplier_name = p_supplier_name and serial_number = p_serial_number and model = p_model;

     if v_supplier_name isnull and v_serial_number isnull and v_model isnull then
      insert into pending(item_name, supplier_name, supplier_address, serial_number, model, amount)
      		values (p_item_name, p_supplier_name, p_supplier_address, p_serial_number, p_model, p_amount);
      return 'Successfully added';
    else
      update pending
      
      set item_name = p_item_name, supplier_address = p_supplier_address, amount = p_amount
        where supplier_name = v_supplier_name and serial_number = v_serial_number and model = v_model;
      
      return 'Successfully updated';
    end if;
  end;
$$
	language 'plpgsql';


create or replace
  function del_pending(in int)
  returns text as
$$
declare
  v_asset_code int;

  begin
  select into v_asset_code asset_code from PAR where asset_code = $1;

  if v_asset_code isnull then
    return 'Record does not exist.';

  else
    delete from PAR where asset_code = $1;
    return 'Record is deleted.';
  end if;
  end;
$$
 language 'plpgsql';
 --select del_par(dce, asset_code);