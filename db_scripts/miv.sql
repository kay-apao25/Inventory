create table miv(
	miv_no serial primary key,
	irr_no_fk int references irr_header(irr_no),
	inv_station_no_fk char references inventory_stat(inv_station_no),
	asset_code_fk int references product(asset_code),
	dce_custodian_fk char references employee(dce),
	dce_user_fk char references employee(dce),
	cost_center_no_fk int references cost_cost(cost_center_no),
	wrs_num char,
	quantity numeric,
	amount numeric,
	date_issued date,
	doc_date date,
	remark text
);

CREATE OR REPLACE
  FUNCTION add_miv(p_irr_no_fk int, p_inv_station_no_fk char, p_asset_code_fk int, p_dce_custodian_fk char, p_dce_user_fk char, p_cost_center_no_fk int, 
  			p_wrs_num char, p_quantity numeric, p_amount numeric, p_date_issued date, p_doc_date date, p_remark text)
  RETURNS int as

$BODY$
  declare
    v_miv_no int;
  begin
    select into v_miv_no miv_no from miv
    where miv_no = v_miv_no; 

    if v_asset_code isnull then
      insert into miv(irr_no_fk, inv_station_no_fk, asset_code_fk, dce_custodian_fk , dce_user_fk, cost_center_no_fk, wrs_num,
					quantity, amount , date_issued , doc_date, remark )
      values (p_irr_no_fk, p_inv_station_no_fk, p_asset_code_fk, p_dce_custodian_fk , p_dce_user_fk, p_cost_center_no_fk, p_wrs_num,
					p_quantity, p_amount , p_date_issued , p_doc_date, p_remark);
      return miv_no;
    else

   			update miv
              set quantity = p_quantity,
				  amount = p_amount,
	              doc_date = p_doc_date,
	              remark = p_remark

        where miv_no = v_miv_no;
      return miv_no;       
    end if;
  end;
$BODY$
language 'plpgsql';



create or replace function get_miv(in int, out int, out int, out char, out int, out int, out char, 
								out char, out int, out char, out numeric, out numeric, out numeric, out date, out date, out text, out text )
  returns setof record as

$$
   select miv.miv_no, miv.irr_no_fk, miv.inv_station_no_fk, miv.asset_code_fk, product.slc_num, miv.dce_custodian_fk, miv.dce_user_fk,
   			miv.cost_center_no_fk, miv.wrs_num, product.unit_cost, miv.quantity, miv.amount, miv.date_issued, miv.doc_date,
   			product.description, miv.remark from irr
	inner join product on product.asset_code = miv.asset_code_fk
	where miv.miv_no = $1
$$
  language 'sql';