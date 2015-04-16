create table irr(
	irr_no int references irr_header(irr_no),
	asset_code int primary key references product(asset_code),
	slc_num int,
	cost_center_no int,
	invoice_num char,
	po_num char,
	dr_num char,
	quantity_actual numeric,
	quantity_accepted numeric,
	quantity_rejected numeric,
	quantity_balance numeric,
	date_recv date,
	wo_no char,
	remark text
);

CREATE OR REPLACE
  FUNCTION add_irr(p_irr_no int, p_asset_code int, p_slc_num int, p_cost_center_no int, p_invoice_num char, p_po_num char, p_dr_num char,
				p_quantity_actual numeric, p_quantity_accepted numeric, p_quantity_rejected numeric, p_quantity_balance numeric, p_date_recv date,
				p_wo_no char, p_remark text)
  RETURNS text as

$BODY$
  declare
    v_asset_code int;
  begin
    select into v_asset_code asset_code from irr
    where asset_code = p_asset_code;

    if v_asset_code isnull then
      insert into employee(irr_no , asset_code , slc_num , cost_center_no , invoice_num , po_num , dr_num ,
				quantity_actual , quantity_accepted , quantity_rejected , quantity_balance , date_recv ,
				wo_no , remark )
      values (p_irr_no , p_asset_code , p_slc_num , p_cost_center_no , p_invoice_num , p_po_num , p_dr_num ,
				p_quantity_actual , p_quantity_accepted , p_quantity_rejected , p_quantity_balance , p_date_recv ,
				p_wo_no , p_remark );
      return 'OK';
    else
    	 update irr
              set quantity_actual = p_quantity_actual,
			 	  quantity_accepted = p_quantity_accepted,
 				  quantity_rejected = p_quantity_rejected,
				  quantity_balance = p_quantity_balance,
				  remark = p_remark

        where asset_code = v_asset_code ;
      return 'OK';       
    end if;
  end;
$BODY$
language 'plpgsql';


