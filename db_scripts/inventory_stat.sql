

create or replace function pseudo_encrypt(value int)
  returns bigint as
$$
  declare
    l1 int;
    l2 int;
    r1 int;
    r2 int;
    i int:=0;
  begin
    l1:= (value >> 16) & 65535;
    r1:= value & 65535;
      while i < 3 loop
        l2 := r1;
        r2 := l1 # ((((1366.0 * r1 + 150889) % 714025) / 714025.0) * 32767)::int;
        l1 := l2;
        r1 := r2;
        i := i + 1;
      end loop;
    return ((l1::bigint << 16) + r1);
  end;
$$ language 'plpgsql' strict immutable;

create sequence random_int_seq;

-- HOW TO USE:
-- select mak_random_id();
create function make_random_id()
  returns bigint as
$$
  select pseudo_encrypt(nextval('random_int_seq')::int)
$$ language sql;





create table inventory_stat(
 	property_cust_fk char references employee(dce),
	PO_num bigint,
	SLC_num int,
	IRR_num int primary key,
	asset_code_fk serial references product(asset_code),
	receive_date date,
	inspection_date date,
	inspection_request_date date,
	quantity int
);


CREATE OR REPLACE
  FUNCTION add_item( p_property_cust_fk char, p_PO_num bigint, p_asset_code_fk int, p_receive_date date, p_inspection_date date, 
  							p_inspection_request_date date, p_quantity int)
  RETURNS text as

$BODY$
  declare
    v_IRR_num int;
    v_SLC_num int;

  begin
    
    select into v_IRR_num IRR_num from inventory_stat
    where IRR_num = v_IRR_num;

    if v_IIR isnull then
      select make_random_id() into v_IRR_num;
      select make_random_id() into v_SLC_num;
      insert into employee( property_cust_fk, PO_num, SLC_num, IRR_num, asset_code_fk, receive_date, inspection_date, 
  							inspection_request_date, quantity)
      values ( p_property_cust_fk, p_PO_num, v_SLC_num, v_IRR_num, p_asset_code_fk, p_receive_date, p_inspection_date, 
  							p_inspection_request_date, p_quantity);
      return 'OK';
    else
      return 'OK';
    end if;
  end;
$BODY$
language 'plpgsql';


create or replace function get_inventstat(in int, out int)
  returns int as

$$
    select quantity from inventory_stat
    where IRR_num = $1;
$$
  language 'sql';

