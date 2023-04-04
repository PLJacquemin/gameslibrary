from decimal import *


def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count == 0:
        return 0
    elif count % 2 == 1:
        return values[int(round(count/2))]
    else:
        return sum(values[count/2-1:count/2+1])/Decimal(2.0)
    

def time_calculation(minutes):
    days = minutes // 1440    
    years =  days // 365
    leftover_days = days % 365
    leftover_minutes = minutes % 1440
    hours = leftover_minutes // 60
    left_minutes = leftover_minutes % 60
    time_calculated={'years': years, 'days': leftover_days, 'hours': hours, 'minutes': left_minutes}
    return time_calculated