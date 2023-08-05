from boo.columns import SHORT_COLUMNS, CONVERTER_FUNC, TTL_COLUMNS
from boo.columns import varname_to_code, code_to_varname


def test_varname_to_code_works_for_one_arg():
    assert varname_to_code("ta") == "1600"

def test_code_to_varname_works_for_one_arg():
    assert code_to_varname('4320') == "cf_fin_out"

def test_sc_all():
    assert SHORT_COLUMNS.all == [
        "name",
        "okpo",
        "okopf",
        "okfs",
        "okved",
        "inn",
        "unit",
        "report_type",
        "of",
        "of_lag",
        "ta_fix",
        "ta_fix_lag",
        "cash",
        "cash_lag",
        "ta_nonfix",
        "ta_nonfix_lag",
        "ta",
        "ta_lag",
        "tp_capital",
        "tp_capital_lag",
        "debt_long",
        "debt_long_lag",
        "tp_long",
        "tp_long_lag",
        "debt_short",
        "debt_short_lag",
        "tp_short",
        "tp_short_lag",
        "tp",
        "tp_lag",
        "sales",
        "sales_lag",
        "profit_oper",
        "profit_oper_lag",
        "exp_interest",
        "exp_interest_lag",
        "profit_before_tax",
        "profit_before_tax_lag",
        "profit_after_tax",
        "profit_after_tax_lag",
        "cf_oper_in",
        "cf_oper_in_sales",
        "cf_oper_out",
        "paid_to_supplier",
        "paid_to_worker",
        "paid_interest",
        "paid_profit_tax",
        "paid_other_costs",
        "cf_oper",
        "cf_inv_in",
        "cf_inv_out",
        "paid_fa_investment",
        "cf_inv",
        "cf_fin_in",
        "cf_fin_out",
        "cf_fin",
        "cf",
        "date_published",
    ]


def test_sc_numeric():
    assert SHORT_COLUMNS.numeric == [
        "of",
        "of_lag",
        "ta_fix",
        "ta_fix_lag",
        "cash",
        "cash_lag",
        "ta_nonfix",
        "ta_nonfix_lag",
        "ta",
        "ta_lag",
        "tp_capital",
        "tp_capital_lag",
        "debt_long",
        "debt_long_lag",
        "tp_long",
        "tp_long_lag",
        "debt_short",
        "debt_short_lag",
        "tp_short",
        "tp_short_lag",
        "tp",
        "tp_lag",
        "sales",
        "sales_lag",
        "profit_oper",
        "profit_oper_lag",
        "exp_interest",
        "exp_interest_lag",
        "profit_before_tax",
        "profit_before_tax_lag",
        "profit_after_tax",
        "profit_after_tax_lag",
        "cf_oper_in",
        "cf_oper_in_sales",
        "cf_oper_out",
        "paid_to_supplier",
        "paid_to_worker",
        "paid_interest",
        "paid_profit_tax",
        "paid_other_costs",
        "cf_oper",
        "cf_inv_in",
        "cf_inv_out",
        "paid_fa_investment",
        "cf_inv",
        "cf_fin_in",
        "cf_fin_out",
        "cf_fin",
        "cf",
    ]


def test_sc_text():
    assert SHORT_COLUMNS.text == [
        "name",
        "okpo",
        "okopf",
        "okfs",
        "okved",
        "inn",
        "unit",
        "report_type",
        "date_published",
    ]


def test_converter_length():
    already_short = CONVERTER_FUNC(TTL_COLUMNS)
    assert len(SHORT_COLUMNS.all) == len(already_short)

