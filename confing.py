import asyncio
from twikit import Client

async def main():
    client = Client(language='en-US')
    await client.login(
        auth_info_1='',  # kullanıcı adı
        auth_info_2='',    # email adı
        password=''   # password
    )
    client.save_cookies('cookies.json')
    print("✅ Giriş başarılı, cookies.json kaydedildi.")

asyncio.run(main())