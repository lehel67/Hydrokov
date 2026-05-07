import aiohttp
import asyncio

BASE_URL = "https://app.hydrokov.ro"
CLIENT_ID = "TSY4647"

async def main():
    async with aiohttp.ClientSession() as session:
        
        login_payload = {
            "email": "konczei.lehel@gmail.com", # ← ÍRD ÁT
            "password": "magdolna1977" # ← ÍRD ÁT
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        print("🔑 Login...")
        async with session.post(f"{BASE_URL}/api/auth", json=login_payload, headers=headers) as resp:
            token = (await resp.text()).strip()
            print(f"✅ Token lekérve")

        auth_headers = {**headers, "X-Auth-Token": token}

        # Fogyasztási adatok
        url = f"{BASE_URL}/api/index/history/{CLIENT_ID}"
        print(f"\n📊 Fogyasztási adatok lekérése: {url}")
        
        async with session.get(url, headers=auth_headers) as resp:
            print("Status:", resp.status)
            if resp.status == 200:
                data = await resp.json()
                
                print("\n=== Fő kulcsok ===")
                print(list(data.keys()))
                
                # Contoare (mérőórák)
                if "contoare" in data:
                    contoare = data["contoare"]
                    print(f"\n🔢 Mérőórák száma: {len(contoare)}")
                    for c in contoare:
                        print(f" - {c.get('nume', 'N/A')} | Szám: {c.get('numar', 'N/A')}")
                
                # Indexes (fogyasztások)
                if "indexes" in data and data["indexes"]:
                    indexes = data["indexes"]
                    print(f"\n📈 Mérőóra állások: {len(indexes)} db")
                    
                    # Utolsó 3 állás
                    for idx in indexes[:3]:
                        print(f"\n Dátum: {idx.get('data', 'N/A')}")
                        print(f" Állás: {idx.get('index', 'N/A')} m³")
                        print(f" Fogyasztás: {idx.get('consum', 'N/A')} m³")
                else:
                    print("Nincs indexes adat")

asyncio.run(main())