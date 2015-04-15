create table irr_header(
	irr_no serial,
	irr_headkey char,
	inv_station_no char,
	reference char,
	invoice_num char,
	po_num char,
	dr_num char,
	dce_custodian char,
	dce_user char,
	proc_date date,
	type char,
	remark text
);