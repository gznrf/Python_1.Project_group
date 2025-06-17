class Logic:

    def simple_interest(principal, rate, years):
        result = principal * (1 + rate * years)
        return result

    def compound_interest(principal, rate, years, periods_per_year):
        result = principal * (1 + rate/periods_per_year)^(periods_per_year * years)
        return result

    def annuity_payment(principal, rate, periods):
        result = principal * (rate * (1 + rate)^periods) / ((1 + rate)^periods - 1)
        return result
    
    def annuity_schedule(principal, rate, periods):
        return 0