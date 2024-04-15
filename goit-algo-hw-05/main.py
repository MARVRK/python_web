import asyncio
import platform
import aiohttp
import sys
import logging
from datetime import timedelta, datetime

logging.basicConfig(level=logging.INFO)


class HttpError(Exception):
    pass

async def request(url:str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status_code} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
                raise HttpError(f"Connection error: {url}", str(err))



def filter_currency(api_data: dict):
    filtered_values = {}
    currency_data = {}
    date = api_data['date']
   
    for entry in api_data["exchangeRate"]:
        if entry["currency"] in ["USD", "EUR"]:
            currency = entry["currency"]
            currency_data[currency] = {
                "sale": entry.get("saleRate", entry["saleRateNB"]),
                "purchase": entry.get("purchaseRate", entry["purchaseRateNB"])
            }
    filtered_values[date] = currency_data
    return filtered_values




async def main(index_day):
    finall_list = []
    selected_date_time = datetime.now() - timedelta(days=int(index_day))
        
    while selected_date_time <= datetime.now() :
        shift = selected_date_time.strftime("%d.%m.%Y") 
        try :
            response = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={shift}")
            exchange_rate = filter_currency(response)
            finall_list.append(exchange_rate)
        except HttpError as err:
            print(err)
        selected_date_time += timedelta(days=1)
    return finall_list


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    logging.info("Program started.")

    if int(sys.argv[1]) <= 10:
      r= asyncio.run(main(sys.argv[1]))
      print(r)
      logging.info("Program finished.")
    else:
        raise ValueError(f"Days range must be no more then 10")

