create table employee(
   dce char primary key,
   name text,
   cost_center_no_fk references cost_cent(cost_center_no),
   charging_cc_no char,
   position text
 );


CREATE OR REPLACE
  FUNCTION add_employee(p_dce char, p_name text, p_cost_center_no char, p_charging_cc_no char, p_position text)
  RETURNS text as

$BODY$
  declare
    v_dce char;
  begin
    select into v_dce dce from employee
    where dce = p_dce;

    if v_dce isnull then
      insert into employee(dce, name, cost_center_no, charging_cc_no, position)
      values (p_dce, p_name, p_cost_center_no, p_charging_cc_no, p_position);
      return 'OK';
    else
              update employee
              set dce = p_dce  ,
                  name =  p_name ,
                  cost_center_no_fk = p_cost_center_no_fk ,
                  charging_cc_no = p_charging_cc_no,
                  position = p_position

        where dce = v_dce;
      return 'OK';
    end if;
  end;
$BODY$
language 'plpgsql';


create or replace function get_employ_depart_pos(in text, out text)
  returns text as

$$
    select position from employee
    where department = $1;
$$
  language 'sql';
 
create or replace function get_employ_depart_name(in text, out text)
  returns text as

$$
    select name from employee
    where department = $1;
$$
  language 'sql';

create or replace function get_employ_pos_dce(in text, out char)
  returns char as

$$
    select dce from employee
    where position = $1;
$$
  language 'sql';

create or replace function get_employ_name_dce(in text, out char)
  returns char as

$$
    select dce from employee
    where name = $1;
$$
  language 'sql';
