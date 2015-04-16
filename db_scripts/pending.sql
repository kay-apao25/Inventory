create table pending(
	item_name text,
  supplier_name text,
  supplier_address text,
  serial_number char,
  model text,
  amount numeric,
  description text,
  Constraint pending_pk Primary Key (supplier_name, serial_number, model)
);

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
        where supplier_name = p_supplier_name and serial_number = p_serial_number and model = p_model;

      return 'Successfully updated';
    end if;
  end;
$$
	language 'plpgsql';

	create or replace
		function get_pending(in text, in char, in text, out text, out text,
												out text, out char, out text, out numeric, out text)
		returns setof record as

	$$
		select * from pending where supplier_name = $1 and serial_number = $2 and model = $3;
	$$
	 language 'sql';
	 --select get_pending(supplier_name, serial_number, model);


create or replace
  function del_pending(in text, in char, in text)
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
    	return 'Record does not exist.';

  	else
    	delete from pending
				where supplier_name = p_supplier_name and serial_number = p_serial_number and model = p_model;
				return 'Record is deleted.';
  	end if;
  end;
$$
 language 'plpgsql';
 --select del_par(supplier_name, serial_number, model);
