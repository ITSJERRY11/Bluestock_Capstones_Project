-- ============================================
-- BLUESTOCK MF CAPSTONE - SQL QUERIES
-- ============================================

-- 1. Top 10 funds by AUM (from fact_performance)
SELECT f.scheme_name, f.fund_house, f.category, p.aum_crore
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 10;

-- 2. Average NAV per month, per fund
SELECT f.scheme_name, d.year, d.month, ROUND(AVG(n.nav), 2) AS avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date_id = d.date_id
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;

-- 3. SIP inflow YoY growth trend (industry-wide)
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM fact_sip_industry
ORDER BY month;

-- 4. Top 5 best performing funds by 3-year return
SELECT f.scheme_name, f.category, p.return_3yr_pct, p.sharpe_ratio, p.morningstar_rating
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 5;

-- 5. Fund house-wise total AUM trend over time
SELECT date, fund_house, aum_crore
FROM fact_aum
ORDER BY fund_house, date;

-- 6. Total transaction volume by transaction type
SELECT transaction_type, COUNT(*) AS num_transactions, ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;

-- 7. Investor demographics: transaction volume by state and city_tier
SELECT state, city_tier, COUNT(*) AS num_transactions, ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY state, city_tier
ORDER BY total_amount_inr DESC
LIMIT 15;

-- 8. Portfolio sector concentration per fund (top holdings)
SELECT f.scheme_name, fp.sector, ROUND(SUM(fp.weight_pct), 2) AS sector_weight_pct
FROM fact_portfolio fp
JOIN dim_fund f ON fp.amfi_code = f.amfi_code
GROUP BY f.scheme_name, fp.sector
ORDER BY f.scheme_name, sector_weight_pct DESC;

-- 9. Risk-adjusted performance: funds with high Sharpe ratio but low max drawdown
SELECT f.scheme_name, f.category, p.sharpe_ratio, p.max_drawdown_pct, p.risk_grade
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.sharpe_ratio > 1.0
ORDER BY p.sharpe_ratio DESC, p.max_drawdown_pct ASC;

-- 10. Monthly transaction trend (count + value) across the platform
SELECT d.year, d.month, COUNT(*) AS num_transactions, ROUND(SUM(t.amount_inr), 2) AS total_amount_inr
FROM fact_transactions t
JOIN dim_date d ON t.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
