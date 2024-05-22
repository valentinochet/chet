import numpy as np
import pandas as pd

# Mortgage calculation
home_price = 1100000
loan_amount = home_price * 0.8  # 80% loan
annual_interest_rate = 0.075
monthly_interest_rate = annual_interest_rate / 12
mortgage_term_years = 30
n_payments = mortgage_term_years * 12

# Mortgage payment formula
monthly_mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**n_payments) / ((1 + monthly_interest_rate)**n_payments - 1)

# Property taxes and maintenance
annual_property_taxes = 0.0125 * home_price
monthly_property_taxes = annual_property_taxes / 12
annual_maintenance_insurance = 0.01 * home_price
monthly_maintenance_insurance = annual_maintenance_insurance / 12

# Closing costs (3% of home price)
closing_costs = 0.03 * home_price

# Total initial investment in buying a house
total_initial_investment = home_price * 0.2 + closing_costs  # 20% down payment + closing costs

# Total monthly homeownership cost before tax benefits
total_monthly_homeownership_cost = monthly_mortgage_payment + monthly_property_taxes + monthly_maintenance_insurance

# Calculate annual mortgage interest for the first year
annual_mortgage_interest = 0
remaining_loan_balance = loan_amount
for month in range(12):
    monthly_interest_payment = remaining_loan_balance * monthly_interest_rate
    annual_mortgage_interest += monthly_interest_payment
    principal_payment = monthly_mortgage_payment - monthly_interest_payment
    remaining_loan_balance -= principal_payment

# Mortgage interest deduction (capped at interest on $750,000)
deductible_mortgage_interest = annual_mortgage_interest * min(loan_amount, 750000) / loan_amount

# SALT deduction (capped at $10,000)
deductible_salt = min(annual_property_taxes, 10000)

# Total tax savings
total_tax_deductions = deductible_mortgage_interest + deductible_salt
effective_tax_savings = total_tax_deductions * 0.24  # Assuming a 24% marginal tax rate

# Adjusted monthly homeownership cost after tax benefits
adjusted_annual_homeownership_cost = (total_monthly_homeownership_cost * 12) - effective_tax_savings
adjusted_monthly_homeownership_cost = adjusted_annual_homeownership_cost / 12

# Renting and investing
monthly_rent = 4000
initial_investment = home_price * 0.2  # 20% down payment
monthly_investment_difference = adjusted_monthly_homeownership_cost - monthly_rent
annual_stock_market_return = 0.035
investment_period_years = 30

# Future value of stock market investment
def future_value_investment(initial_investment, monthly_investment, annual_return, years):
    months = years * 12
    future_value = initial_investment * (1 + annual_return)**years
    for month in range(1, months + 1):
        future_value += monthly_investment * (1 + annual_return)**((months - month) / 12)
    return future_value

future_value_stock_investment = future_value_investment(initial_investment, monthly_investment_difference, annual_stock_market_return, investment_period_years)

# Required home appreciation rate calculation
def required_home_appreciation(initial_home_value, future_value_investment, years):
    return (future_value_investment / initial_home_value)**(1 / years) - 1

initial_home_value = home_price
required_appreciation_rate = required_home_appreciation(initial_home_value, future_value_stock_investment, investment_period_years)

# Create DataFrame with properly formatted numbers
df = pd.DataFrame({
    'Description': [
        'Initial Investment in Stock Market',
        'Monthly Investment Difference',
        'Future Value of Stock Market Investment',
        'Required Annual Home Appreciation Rate (%)',
        'Closing Costs',
        'Total Initial Investment in Buying a House',
        'Annual Mortgage Interest Deduction',
        'Annual SALT Deduction',
        'Effective Tax Savings',
        'Adjusted Monthly Homeownership Cost'
    ],
    'Amount': [
        f"${initial_investment:,.2f}",
        f"${monthly_investment_difference:,.2f}",
        f"${future_value_stock_investment:,.2f}",
        f"{required_appreciation_rate * 100:.2f}%",
        f"${closing_costs:,.2f}",
        f"${total_initial_investment:,.2f}",
        f"${deductible_mortgage_interest:,.2f}",
        f"${deductible_salt:,.2f}",
        f"${effective_tax_savings:,.2f}",
        f"${adjusted_monthly_homeownership_cost:,.2f}"
    ]
})

print("Investment Comparison:")
print(df.to_string(index=False, justify="center"))
