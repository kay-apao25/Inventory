create table miv(
	miv_no serial primary key,
	irr_no int references irr_header(irr_no),
	inv_station_no char,
	asset_code int references product(asset_code),
	dce_custodian char,
	dce_user char,
	cost_center_no int,
	wrs_num char,
	quantity numeric,
	amount numeric,
	date_issued date,
	doc_date date,
	remark text
);

CREATE OR REPLACE
  FUNCTION add_irr(p_irr_no int, p_inv_station_no char, p_asset_code int, p_dce_custodian char, p_dce_user char, p_cost_center_no int, p_wrs_num char,
					p_quantity numeric, p_amount numeric, p_date_issued date, p_doc_date date, p_remark text)
  RETURNS text as

$BODY$
  declare
    v_miv_no int;
  begin
    select into v_miv_no miv_no from miv
    where miv_no = v_miv_no; 

    if v_asset_code isnull then
      insert into employee(irr_no, inv_station_no, asset_code, dce_custodian , dce_user, cost_center_no, wrs_num,
					quantity, amount , date_issued , doc_date, remark )
      values (p_irr_no, p_inv_station_no, p_asset_code, p_dce_custodian , p_dce_user, p_cost_center_no, p_wrs_num,
					p_quantity, p_amount , p_date_issued , p_doc_date, p_remark);
      return 'OK';
    else

   			update miv
              set quantity = p_quantity,
				  amount = p_amount,
	              doc_date = p_doc_date,
	              remark = p_remark

        where miv_no = v_miv_no;
      return 'OK';       
    end if;
  end;
$BODY$
language 'plpgsql';