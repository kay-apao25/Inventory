create table supplier{
	supplier_num char primary key,
	supplier_name text,
	supplier_address text,
	telephone_number char,
	credit_limit numeric,
	debit_amt numeric,
	credit_amt numeric,
	balance_amt numeric,
	contact_person text,
	remarks text
};

-- HOW TO USE:
-- SELECT add_supplier('383nfediof', 'Keira Montiel', 'Iligan City', '225-2748', 10000.00, 1000.00, 2000.00, 1326.88, 'Lily Tiger', 'ok');
create or replace function add_supplier(p_supplier_num char, p_supplier_name text, p_supplier_address text, p_telephone_number char,
			p_credit_limit numeric, p_debit_amt numeric, p_credit_amt numeric, p_balance_amt numeric, p_contact_person text, p_remarks text)
return text as
$$
    declare
    	v_supplier_num char;
	begin
		select supplier_num from supplier into v_supplier_num
			where supplier_num = p_supplier_num;
		if v_supplier_num isnull then
			insert into supplier(supplier_num, supplier_name, supplier_address, telephone_number, credit_limit, debit_amt, credit_amt,
				balance_amt, contact_person, remarks) 
			values (p_supplier_num, p_supplier_name, p_supplier_address, p_telephone_number, p_credit_limit, p_debit_amt, p_credit_amt, 
				p_balance_amt, p_contact_person, p_remarks);
			return 'Successfully added';
		else
			update supplier
				set supplier_name = p_supplier_name, supplier_address = p_supplier_address, 
				telephone_number = p_telephone_number, credit_limit = p_credit_limit, debit_amt = p_debit_amt, credit_amt = p_credit_amt,
				balance_amt = p_balance_amt, contact_person = p_contact_person, remarks = p_remarks
				where supplier_num = v_supplier_num;
			return 'Successfully updated';
    end if;
    end;
$$
	language 'plpgsql';