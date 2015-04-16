create table irr_header(
	irr_no serial primary key,
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

create or replace function add_irr_header(p_irr_headkey char, p_inv_station_no char, p_reference char, p_invoice_num char, p_po_num char,
		p_dr_num char, p_dce_custodian char, p_dce_user char, p_proc_date date, p_type char, p_remark text)
	return text as
$$
	declare
		v_irr_no int;
	begin
		select irr_no from irr_header into v_irr_no
			where irr_headkey = p_irr_headkey;
		if v_irr_no isnull then
			insert into irr_header(irr_header, inv_station_no, reference, invoice_num, po_num, dr_num, dce_custodian, dce_user, 
				proc_date, type, remark)
			values (p_irr_headkey, p_inv_station_no, p_reference, p_invoice_num, p_po_num, p_dr_num, p_dce_custodian, p_dce_user, p_proc_date,
				p_type, p_remark);
		else
			update irr_header
				set irr_headkey = p_irr_headkey, inv_station_no = p_inv_station_no, reference = p_reference, invoice_num = p_invoice_num,
					po_num = p_po_num, dr_num = p_dr_num, dce_custodian = p_dce_custodian, dce_user = p_dce_user, proc_date = p_proc_date, 
					type = p_type, remark = p_remark
				where irr_no = v_irr_no;
		end if;
	end;
$$ 
	language 'plpgsql';