create table customer(
   dce_fk char(8) references employee(dce) primary key,
   name text,
   cost_center_no char(7),
   credit_limit numeric,
   debit_amt numeric,
   credit_amt numeric,
   balance_amt numeric
);


CREATE OR REPLACE
  FUNCTION add_customer(p_dce_fk char, p_name text, p_cost_center_no char, p_credit_limit numeric, p_debit_amt, p_credit_amt numeric,
    p_balance_amt numeric)
  RETURNS text as

$BODY$
  declare
    v_dce_fk char;
  begin
    select into v_dce_fk dce_fk from customer
    where dce_fk = p_dce_fk;

    if v_dce_fk isnull then
      insert into customer(dce_fk, name, cost_center_no, credit_limit, debit_amt, credit_amt, balance_amt)
      values (p_dce_fk, p_name, p_cost_center_no, p_credit_limit, p_debit_amt, p_credit_amt, p_balance_amt);
      return 'OK';
    else
              update customer
              set name = p_name,
                  cost_center_no = p_cost_center_no,
                  credit_limit = p_credit_limit,
                  debit_amt = debit_amt,
                  credit_amt = p_credit_amt,
                  balance_amt = p_balance_amt
        where dce_fk = v_dce_fk;
      return 'OK';
    end if;
  end;
$BODY$
language 'plpgsql';
