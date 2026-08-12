CREATE TABLE dim_date (
    date_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    date           TEXT,
    year           INTEGER,
    month          INTEGER,
    quarter        INTEGER,
    day_of_week    TEXT,
    is_weekday     INTEGER
);

CREATE TABLE dim_fund (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT,
    scheme_name         TEXT,
    category            TEXT,
    sub_category         TEXT,
    plan                TEXT,
    launch_date         TEXT,
    benchmark           TEXT,
    expense_ratio_pct   REAL,
    exit_load_pct       REAL,
    min_sip_amount      REAL,
    min_lumpsum_amount  REAL,
    fund_manager        TEXT,
    risk_category       TEXT,
    sebi_category_code  TEXT
);

CREATE TABLE fact_portfolio (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code            INTEGER,
    stock_symbol         TEXT,
    stock_name           TEXT,
    sector               TEXT,
    weight_pct           REAL,
    market_value_cr      REAL,
    current_price_inr    REAL,
    portfolio_date       TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    date              TEXT,
    fund_house        TEXT,
    aum_lakh_crore    REAL,
    aum_crore         REAL,
    num_schemes       INTEGER
);

CREATE TABLE fact_sip_industry (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    month                       TEXT,
    sip_inflow_crore            REAL,
    active_sip_accounts_crore   REAL,
    new_sip_accounts_lakh       REAL,
    sip_aum_lakh_crore          REAL,
    yoy_growth_pct              REAL
);