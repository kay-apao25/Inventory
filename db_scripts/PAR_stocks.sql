create table PAR(
  dce_FK char(8) primary key references employee(dce),
  asset_code_FK int primary key references product(asset_code),
  par_date date,
  par_no char,
  amt_cost numeric,
  remark text,
  qty int
);

create or replace
	function add_par(dce_ char, asset_code_ int, par_no_ char, amt_cost numeric, remark_ text, qty_ int)
	returns text as
$$
	declare
		v_asset_code int;
    v_dce char;
	begin
    select dce_FK, asset_code_FK from PAR into v_dce, v_asset_code
			where asset_code_FK = asset_code_ and dce_FK = dce_;

		if v_asset_code isnull and v_dce isnull then
			insert into PAR(dce_FK, asset_code_FK, par_date, par_no, remark, qty) values
				(dce_, asset_code_, now()::date, par_no_, remark_, qty);
			return 'PAR added';
		else
			update PAR

			set dce_FK = dce_, asset_code_FK = asset_code_, par_date = now()::date, par_no = par_no_,
				amt_cost = amt_cost_, remark = remark_, qty = qty_ where asset_code_FK = asset_code_ and dce_FK = dce_;
			return 'PAR updated';
		end if;

	end;

$$
language 'plpgsql';
-- select add_par(dce_, asset_code_, date_, par_no_, amt_cost, remark_);

create or replace
	function get_par(in char, in int, out char, out int, out date, out char, out numeric, out text)
	returns setof record as

$$
  select PAR.par_date, PAR.par_no, PAR.amt_cost, PAR.remark, PAR.qty, employee.name,
    employee.position, product.asset_code, product.description from PAR
    inner join employee on employee.dce = PAR.dce_FK
      where PAR.dce_FK = $1;
    inner join product on product.asset_code = PAR.asset_code_FK
      where PAR.asset_code_FK = $2;
$$
 language 'sql';
 --select get_par(employee, code);

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
	function add_garv(dce_ char, asset_code_ int, garv_date_ date, garv_no_ char)
	returns text as
$$
	declare
		v_asset_code int;
	begin
		select into v_asset_code asset_code_FK from PAR where
			asset_code_ = asset_code_FK;

		if v_asset_code isnull then
			insert into stock_items(dce_FK, asset_code_FK, garv_date, garv_no) values
				(dce_, asset_code_, now()::date, garv_no_);
				return 'GARV is added';
		else
			update stock_items

			set garv_date = now()::date, garv_no = garv_no_
				where asset_code_ = asset_code_FK and dce_FK = dce_;
			return 'GARV is updated';
		end if;

	end;

$$
language 'plpgsql';
-- select add_garv(dce, asset_code, garv_date, garv_no);

create or replace
	function get_garv(in char, in int, out char, out int, out date, out char)
	returns setof record as

$$
	select * from PAR where dce_FK = $1 and asset_code_FK = $2;
$$
 language 'sql';
 --select get_par(dce, asset_code);
