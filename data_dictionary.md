# Data Dictionary — Bluestock MF Capstone

Database: `db/bluestock_mf.db` (SQLite, star schema, 8 tables)

---

## dim_fund
Dimension table — one row per mutual fund scheme.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK) | Unique AMFI code identifying the scheme |
| fund_house | TEXT | Asset management company (AMC) name |
| scheme_name | TEXT | Full scheme name |
| category | TEXT | Broad category (Equity, Debt, Hybrid, etc.) |
| sub_category | TEXT | Sub-category (Large Cap, Small Cap, Gilt, etc.) |
| plan | TEXT | Plan type (Regular / Direct) |
| launch_date | TEXT | Scheme launch date (YYYY-MM-DD) |
| benchmark | TEXT | Benchmark index the fund is measured against |
| expense_ratio_pct | REAL | Annual expense ratio (%) |
| exit_load_pct | REAL | Exit load charge (%) |
| min_sip_amount | REAL | Minimum SIP investment amount (INR) |
| min_lumpsum_amount | REAL | Minimum lumpsum investment amount (INR) |
| fund_manager | TEXT | Name of the fund manager |
| risk_category | TEXT | Risk level (Low, Moderate, High, Very High) |
| sebi_category_code | TEXT | SEBI-assigned scheme category code |

---

## dim_date
Dimension table — one row per calendar date present in NAV or transaction data.

| Column | Type | Description |
|---|---|---|
| date_id | INTEGER (PK) | Surrogate key for the date |
| date | TEXT | Calendar date (YYYY-MM-DD) |
| year | INTEGER | Year |
| month | INTEGER | Month (1–12) |
| quarter | INTEGER | Quarter (1–4) |
| day_of_week | TEXT | Day name (Monday, Tuesday, etc.) |
| is_weekday | INTEGER | 1 if weekday, 0 if weekend |

---

## fact_nav
Fact table — daily NAV per fund.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK → dim_fund) | Scheme identifier |
| date_id | INTEGER (FK → dim_date) | Date identifier |
| nav | REAL | Net Asset Value on that date |

---

## fact_transactions
Fact table — individual investor transactions.

| Column | Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| date_id | INTEGER (FK → dim_date) | Transaction date identifier |
| amfi_code | INTEGER (FK → dim_fund) | Scheme identifier |
| transaction_type | TEXT | Type of transaction (Purchase, Redemption, SIP, etc.) |
| amount_inr | REAL | Transaction amount (INR) |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | City tier classification (Tier 1/2/3) |
| age_group | TEXT | Investor age bracket |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Investor's annual income (in lakh INR) |
| payment_mode | TEXT | Mode of payment used |
| kyc_status | TEXT | KYC verification status |

---

## fact_performance
Fact table — scheme-level performance metrics (one row per fund).

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK → dim_fund) | Scheme identifier |
| return_1yr_pct | REAL | 1-year return (%) |
| return_3yr_pct | REAL | 3-year annualized return (%) |
| return_5yr_pct | REAL | 5-year annualized return (%) |
| benchmark_3yr_pct | REAL | Benchmark 3-year return (%) |
| alpha | REAL | Alpha (excess return vs benchmark) |
| beta | REAL | Beta (volatility relative to benchmark) |
| sharpe_ratio | REAL | Risk-adjusted return measure |
| sortino_ratio | REAL | Downside risk-adjusted return measure |
| std_dev_ann_pct | REAL | Annualized standard deviation (%) |
| max_drawdown_pct | REAL | Maximum drawdown (%) |
| aum_crore | REAL | Assets under management (INR crore) |
| expense_ratio_pct | REAL | Expense ratio (%) |
| morningstar_rating | INTEGER | Morningstar star rating (1–5) |
| risk_grade | TEXT | Risk grading label |

---

## fact_portfolio
Fact table — portfolio holdings per scheme.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK → dim_fund) | Scheme identifier |
| stock_symbol | TEXT | Stock ticker symbol |
| stock_name | TEXT | Stock/company name |
| sector | TEXT | Industry sector |
| weight_pct | REAL | Weight of holding in portfolio (%) |
| market_value_cr | REAL | Market value of holding (INR crore) |
| current_price_inr | REAL | Current stock price (INR) |
| portfolio_date | TEXT | Date the portfolio snapshot was taken |

---

## fact_aum
Fact table — AUM by fund house over time.

| Column | Type | Description |
|---|---|---|
| date | TEXT | Reporting date |
| fund_house | TEXT | Asset management company name |
| aum_lakh_crore | REAL | AUM in lakh crore INR |
| aum_crore | REAL | AUM in crore INR |
| num_schemes | INTEGER | Number of schemes offered by the fund house |

---

## fact_sip_industry
Fact table — industry-wide monthly SIP statistics.

| Column | Type | Description |
|---|---|---|
| month | TEXT | Reporting month |
| sip_inflow_crore | REAL | Total SIP inflow (INR crore) |
| active_sip_accounts_crore | REAL | Active SIP accounts (in crore) |
| new_sip_accounts_lakh | REAL | New SIP accounts registered (in lakh) |
| sip_aum_lakh_crore | REAL | SIP AUM (lakh crore INR) |
| yoy_growth_pct | REAL | Year-over-year SIP growth (%) |

---

## Entity Relationships

- `fact_nav.amfi_code` → `dim_fund.amfi_code`
- `fact_nav.date_id` → `dim_date.date_id`
- `fact_transactions.amfi_code` → `dim_fund.amfi_code`
- `fact_transactions.date_id` → `dim_date.date_id`
- `fact_performance.amfi_code` → `dim_fund.amfi_code`
- `fact_portfolio.amfi_code` → `dim_fund.amfi_code`
