create table cost_cent(
	cost_center_no serial primary key,
  cost_center_name text,
  functional_group char
);

-- HOW TO:
-- select add_cost_cent (12345, 'ISTD', 'sdfisod33r3')
create or replace function add_cost_cent (p_cost_center_name text, p_functional_group char)
  return text as
$$
  declare
    v_cost_center_no int;
  begin
    select cost_center_no from cost_cent into v_cost_center_no 
      where cost_center_name = p_cost_center_name;
    if v_cost_center_no isnull then
      insert into cost_cent(cost_center_no, cost_center_name, functional_group)
      values (p_cost_center_no, p_cost_center_name, p_functional_group);
    return 'Successfully added';
    else
      update cost_cent
        set cost_center_name = p_cost_center_name, functional_group = p_functional_group
          where cost_center_no = v_cost_center_no;
    return 'Successfully updated';
    end if;
    end;
$$ 
  language 'plpgsql';
