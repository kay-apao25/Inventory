create table PAR(
  dce_FK char references employee(dce),
  asset_code_FK int primary key references product(asset_code)
);

create or replace
	function add_par(in text, in text, out text)
	returns text as
$$
	declare
		dce_ alias for $1;
		asset_code_ alias for $2;

		v_asset_code int;
	begin
		select into v_asset_code asset_code_FK from PAR where
			asset_code_ = asset_code_FK; 

		if v_asset_code isnull then
			insert into PAR(dce_FK, asset_code_FK) values
				(dce_, asset_code_)
		else
			update PAR set
			dce_FK = dce_ and
			asset_code_FK = asset_code_
		end if;
		returns 'OK';
	end;

$$
language 'plpgsql';
-- select add_par(dce, asset_code);

create or replace
	function get_par(in text, out text)
	returns setof record as

$$
	select * from where name_employee_FK = $1;
$$
 language 'sql';
 --select get_par(employee);

create or replace
 	function del_par(in text, in text)
 	returns text as
$$
	delete * from PAR where
		dce_FK = $1 and asset_code_FK = $2;
$$
 language 'sql';
 --select del_par(dce, asset_code);

create table stock_items(
  dce_FK char references employee(dce),
  asset_code_FK int primary key references product(asset_code)
);

create or replace
	function add_garv(in text, in text, out text)
	returns text as
$$
	declare
		dce_ alias for $1;
		asset_code_ alias for $2;

		v_asset_code int;
	begin
		select into v_asset_code asset_code_FK from PAR where
			asset_code_ = asset_code_FK; 

		if v_asset_code isnull then
			insert into stock_items(dce_FK, asset_code_FK) values
				(dce_, asset_code_)
		else
			update stock_items set
			dce_FK = dce_ and
			asset_code_FK = asset_code_
		end if;
		returns 'OK';
	end;

$$
language 'plpgsql';
-- select add_garv(dce, asset_code);