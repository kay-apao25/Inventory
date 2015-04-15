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