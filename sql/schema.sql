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