

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
  inv_station_no char primary key,
  station_description text,
  cost_center_no_fk int references cost_cent(cost_center_no)
);


CREATE OR REPLACE
  FUNCTION add_item(p_inv_station_no char, p_station_description text, p_cost_center_no_fk int)
  RETURNS text as

$BODY$
  declare
    v_inv_station_no char;

  begin
    
    select into v_inv_station_no inv_station_no from inventory_stat
    where inv_station_no = p_inv_station_no;

    if v_inv_station_no isnull then
      insert into employee( inv_station_no, station_description, cost_center_no_fk)
      values (p_inv_station_no, p_station_description, p_cost_center_no_fk);
      return 'OK';
    else
      return 'OK';
    end if;
  end;
$BODY$
language 'plpgsql';

