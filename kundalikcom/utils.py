def months_size_price(months_count: int, month_price: int, month_chegirma: int) -> int:
    if months_count < 3:
        return month_price*months_count
    return month_chegirma*months_count
