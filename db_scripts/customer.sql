create table customer(
   dce char primary key,
   name text,
   department text,
   position text
);


CREATE OR REPLACE
  FUNCTION add_customer(p_dce char, p_name text, p_department text, p_position text)
  RETURNS text as

$BODY$
  declare
    v_dce char;
  begin
    select into v_dce dce from customer
    where dce = p_dce;

    if v_dce isnull then
      insert into customer(dce, name , department , position)
      values (p_dce, p_name , p_department , p_position);
      return 'OK';
    else
              update customer
              set dce = p_dce,
                  name = p_name,
                  department = p_department,
                  position = p_position

        where dce = v_dce;
      return 'OK';
    end if;
  end;
$BODY$
language 'plpgsql';