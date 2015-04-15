create table irr(
	irr_no int references irr_header(irr_no),
	asset_code int references product(asset_code),
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


