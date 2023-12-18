import aiohttp
import logging
import asyncio
from datetime import datetime, timedelta
import sys


# Are the days of the search set
def check_days(days: str):
    if not days.isdigit() or int(days) < 0 or int(days) > 10:
        return False
    return True


# Make HTTP GET request
async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    return response
        except aiohttp.ClientConnectionError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


# Obtaining a quote for a given currency pair and date
async def get_quote(currency_ticker: str, date: str):
    result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}')
    if result:
        rates = result.get("exchangeRate")
        filtered_rates = list(filter(lambda element: element["currency"] == currency_ticker, rates))
        if filtered_rates:
            currency_data, = filtered_rates
            return {'Currency': currency_ticker, 'buy': currency_data['purchaseRateNB'],
                    'sale': currency_data['saleRateNB'], 'Date': date}
    return "Failed to retrieve data"


# Loop for obtaining a quote for a given currency pairs and dates
def main_loop_for_get_quote(currency_ticker, days: int):
    day_for_request = datetime.now()
    for _ in range(days):
        result = asyncio.run(get_quote(currency_ticker, day_for_request.strftime("%d.%m.%Y")))
        write_to_result_list(result['Date'], result['Currency'], result['sale'], result['buy'])
        day_for_request -= timedelta(days=1)


# Write result in the list
def write_to_result_list(data, currency_ticker, sale, purchase):
    for i in range(len(result_of_search)):
        if data in result_of_search[i]:
            result_of_search[i][data][currency_ticker] = {'sale': sale, 'purchase': purchase}
            return
    result_of_search.append({data: {currency_ticker: {'sale': sale, 'purchase': purchase}}})


# Main function
def main():
    currencies = ["EUR", "USD"]
    if len(sys.argv) > 1 and check_days(sys.argv[1]):
        for currency in currencies:
            main_loop_for_get_quote(currency, int(sys.argv[1]))


# Start of the program
if __name__ == "__main__":
    result_of_search = []
    main()
    print(result_of_search)
