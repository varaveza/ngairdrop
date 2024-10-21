import asyncio
import aiohttp
import json
from aiohttp import ClientConnectorError, ServerTimeoutError

async def telegram_auth_request(session):
    url = 'https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP'
    headers = {
        'Host': 'user-domain.blum.codes',
        'Content-Type': 'application/json',
        'Lang': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://telegram.blum.codes',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    body = {"query":"query_id=AAFGOn8JAwAAAEY6fwm7mDdU&user=%7B%22id%22%3A6601783878%2C%22first_name%22%3A%22L%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22sayalalapo%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1729509849&hash=75f14e3de87f3413f0cacb2e655bdca489e06fef18c3432fbc61c47e38d6fa00"}
    
    try:
        async with session.post(url, headers=headers, json=body, timeout=30) as response:
            result = await response.json()
            print(f"Telegram Auth Status: {response.status}")
            print("Telegram Auth Response:", result)
            
            access_token = result.get('token', {}).get('access')
            if not access_token:
                raise ValueError("Token akses tidak ditemukan dalam respons")
            
            return access_token
    except asyncio.TimeoutError:
        print("Timeout saat melakukan autentikasi Telegram")
        raise
    except (ClientConnectorError, ServerTimeoutError) as e:
        print(f"Kesalahan koneksi saat autentikasi Telegram: {str(e)}")
        raise
    except Exception as e:
        print(f"Kesalahan tidak terduga saat autentikasi Telegram: {str(e)}")
        raise

async def make_daily_reward_request(session, i, access_token):
    url = 'https://game-domain.blum.codes/api/v1/daily-reward?offset=-420'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Lang': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://telegram.blum.codes',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        async with session.post(url, headers=headers, timeout=30) as response:
            result = await response.json()
            print(f"Daily Reward Request {i+1} Status: {response.status}")
            print(f"Daily Reward Response {i+1}:", result)
            return result
    except asyncio.TimeoutError:
        print(f"Timeout saat melakukan permintaan daily reward ke-{i+1}")
        raise
    except (ClientConnectorError, ServerTimeoutError) as e:
        print(f"Kesalahan koneksi saat permintaan daily reward ke-{i+1}: {str(e)}")
        raise
    except Exception as e:
        print(f"Kesalahan tidak terduga saat permintaan daily reward ke-{i+1}: {str(e)}")
        raise

async def main(num_requests):
    async with aiohttp.ClientSession() as session:
        try:
            access_token = await telegram_auth_request(session)
            print("Token Akses berhasil diperoleh.")
            
            tasks = [make_daily_reward_request(session, i, access_token) for i in range(num_requests)]
            daily_reward_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful_requests = sum(1 for result in daily_reward_results if not isinstance(result, Exception))
            print(f"{successful_requests} dari {num_requests} permintaan daily reward berhasil.")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Terjadi kesalahan yang tidak terduga: {str(e)}")

NUM_REQUESTS = 100

if __name__ == "__main__":
    asyncio.run(main(NUM_REQUESTS))
        
        
        
        # query_id=AAFGOn8JAwAAAEY6fwm7mDdU&user=%7B%22id%22%3A6601783878%2C%22first_name%22%3A%22L%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22sayalalapo%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1729509849&hash=75f14e3de87f3413f0cacb2e655bdca489e06fef18c3432fbc61c47e38d6fa00 lala ada 11
        # query_id=AAFN4AA5AwAAAE3gADncD_7I&user=%7B%22id%22%3A7398809677%2C%22first_name%22%3A%22Mi%20ayam%22%2C%22last_name%22%3A%22Goreng%22%2C%22username%22%3A%22ronaldocsgoat%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1729510013&hash=ea3d78170ef4ebb74703c938bde3b497baf3a97b5891654964c8d940dae34f3e miayamgoreng ada 35#
        # user=%7B%22id%22%3A7853368916%2C%22first_name%22%3A%22Samyang%22%2C%22last_name%22%3A%22Goreng%22%2C%22username%22%3A%22xmxmmxmemex%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=-2062927947356008307&chat_type=sender&auth_date=1729510376&hash=8918216f9b47e98aae8a1ec0171f0e37dd926e554040a0939bfe6d997a3e09e0 samyang ada 28
