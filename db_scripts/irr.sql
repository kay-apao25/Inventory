create table irr(
	irr_no_fk int references irr_header(irr_no),
	asset_code_fk int primary key references product(asset_code),
	cost_center_no_fk int references cost_cent(cost_center_no),
	quantity_actual numeric,
	quantity_accepted numeric,
	quantity_rejected numeric,
	quantity_balance numeric,
	date_recv date,
	wo_no char,
	remark text
);

CREATE OR REPLACE
  FUNCTION add_irr(p_irr_no_fk int, p_asset_code_fk int, p_cost_center_no_fk int, p_quantity_actual numeric, p_quantity_accepted numeric, 
  		1			p_quantity_rejected numeric, p_quantity_balance numeric, p_date_recv date,p_wo_no char, p_remark text)
  RETURNS text as

$BODY$
  declare
    v_asset_code_fk int;
  begin
    select into v_asset_code_fk asset_code_fk from irr
    where asset_code_fk = p_asset_code_fk;

    if v_asset_code isnull then
      insert into irr(irr_no_fk , asset_code_fk , cost_center_no_fk ,
				quantity_actual , quantity_accepted , quantity_rejected , quantity_balance , date_recv ,
				wo_no , remark )
      values (p_irr_no_fk , p_asset_code_fk , p_cost_center_no_fk , 
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

        where asset_code_fk = v_asset_code_fk ;
      return 'OK';       
    end if;
  end;
$BODY$
language 'plpgsql';


create or replace function get_irr(in int, out int, out int, out int, out char, out numeric, out numeric, 
								out numeric, out numeric, out numeric, out date, out text, out char, out text )
  returns setof record as

$$
   select product.asset_code , product.slc_num , irr.cost_center_no_fk , product.unit_measure, product.unit_cost,
				irr.quantity_actual , irr.quantity_accepted , irr.quantity_rejected , irr.quantity_balance , irr.date_recv , product.description,
				irr.wo_no , irr.remark  from irr
	inner join product on product.asset_code = irr.asset_code_fk
	where irr.asset_code_fk = $1
$$
  language 'sql';


