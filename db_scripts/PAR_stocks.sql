create table PAR(
  dce_FK char references employee(dce),
  asset_code_FK int primary key references product(asset_code),
  par_date date,
  par_no char,
  amt_cost numeric,
  description text,
  remark text
);

create or replace
	function add_par(dce_ char, asset_code_ int, date_ date, par_no_ char)
	returns text as
$$
	declare
		v_asset_code int;
	begin
		select into v_asset_code asset_code_FK from PAR where
			asset_code_ = asset_code_FK; 

		if v_asset_code isnull then
			insert into PAR(dce_FK, asset_code_FK, par_date) values
				(dce_, asset_code_, now()::date);
			return 'OK';
		else
			return 'Record already exist.';
		end if;
		
	end;

$$
language 'plpgsql';
-- select add_par(dce, asset_code);

create or replace
	function get_par(in char, out char, out int, out date)
	returns setof record as

$$
	select * from PAR where dce_FK = $1;
$$
 language 'sql';
 --select get_par(employee);

create or replace
 	function del_par(in char, in int)
 	returns text as
$$
declare
	v_dce char;

	begin
	select into v_dce dce_FK from PAR where
		dce_FK = $1 and asset_code_FK = $2;

	if v_dce isnull then
		return 'Record does not exist.';

	else
		delete from PAR where dce_FK = $1 and asset_code_FK = $2;
		return 'Record is deleted.';
	end if;
	end;
$$
 language 'plpgsql';
 --select del_par(dce, asset_code);

create table stock_items(
  dce_FK char references employee(dce),
  asset_code_FK int primary key references product(asset_code),
  garv_date date,
  garv_no char
);

create or replace
	function add_garv(dce_ char, asset_code_ int, garv_date date)
	returns text as
$$
	declare
		v_asset_code int;
	begin
		select into v_asset_code asset_code_FK from PAR where
			asset_code_ = asset_code_FK; 

		if v_asset_code isnull then
			insert into stock_items(dce_FK, asset_code_FK, garv_date) values
				(dce_, asset_code_, now()::date);
				return 'OK';
		else
				return 'Record already exist.';
		end if;
		
	end;

$$
language 'plpgsql';
-- select add_garv(dce, asset_code);