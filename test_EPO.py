import asyncio
import httpx
import base64
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# KRITICKÉ: Načítaj .env súbor
load_dotenv()

# ==============================================================================
# POMOCNÉ FUNKCIE PRE EXTRAKCIU DÁT A VÝPOČET
# ==============================================================================

def get_patent_dates(data: dict) -> dict:
    """
    KONEČNÁ FUNKCIA pre extrakciu dátumov, opravená na základe analyzovaného JSON
    súboru EP0683520_data.json, ktorá správne navigujú na list dokumentov.
    """
    
    application_date = 'N/A'
    grant_date = 'N/A'
    
    # KRITICKÝ KROK: Správna cesta k zoznamu dokumentov
    exchange_documents = data.get('ops:world-patent-data', {}).get('exchange-documents', {}).get('exchange-document', [])
    
    # Ak je to dict (iba jeden dokument), zabaľ ho do listu
    if isinstance(exchange_documents, dict):
        exchange_documents = [exchange_documents]
    elif not isinstance(exchange_documents, list):
        return {'application_date': 'N/A', 'grant_date': 'N/A'} # Zlyhanie navigácie

    # 1. Hľadanie Dátumu podania (Application Date)
    for doc in exchange_documents:
        # Dátum podania je v application-reference. Hľadáme ho v epodoc ID
        app_ref = doc.get('bibliographic-data', {}).get('application-reference', {})
        for doc_id in app_ref.get('document-id', []):
            if doc_id.get('@document-id-type') == 'epodoc':
                date_element = doc_id.get('date', {})
                if date_element and date_element.get('$'):
                    application_date = date_element['$']
                    break
        if application_date != 'N/A':
            break

    # 2. Hľadanie Dátumu udelenia (Grant Date)
    # Dátum udelenia je dátum publikácie dokumentu s @kind="B1"
    for doc in exchange_documents:
        if doc.get('@kind') == 'B1':
            pub_ref = doc.get('bibliographic-data', {}).get('publication-reference', {})
            
            # Hľadáme dátum publikácie B1 dokumentu
            for doc_id in pub_ref.get('document-id', []):
                if doc_id.get('date'):
                    grant_date = doc_id['date'].get('$')
                    break
            if grant_date != 'N/A':
                break

    return {
        'application_date': application_date,
        'grant_date': grant_date
    }

def calculate_theoretical_expiration(app_date_str: str) -> str:
    """Vypočíta teoretickú exspiráciu (20 rokov od podania)."""
    if app_date_str == 'N/A':
        return 'N/A (Dátum podania neznámy)'
    
    try:
        # Konverzia dátumu z YYYYMMDD na datetime objekt
        app_date = datetime.strptime(app_date_str, '%Y%m%d')
        # Teoretická exspirácia je v deň 20. výročia dátumu podania.
        expiration_date = app_date.replace(year=app_date.year + 20)
        return expiration_date.strftime('%Y-%m-%d')
    except ValueError:
        return 'N/A (Chybný formát dátumu)'

# ==============================================================================
# HLAVNÁ ASYNCHRÓNNA FUNKCIA
# ==============================================================================

async def test_epo():
    consumer_key = os.getenv('EPO_CONSUMER_KEY')
    consumer_secret = os.getenv('EPO_CONSUMER_SECRET')
    
    print(f"🔑 Key: {consumer_key[:10]}... (loaded: {bool(consumer_key)})")
    print(f"🔐 Secret: {consumer_secret[:10]}... (loaded: {bool(consumer_secret)})")
    
    if not consumer_key or not consumer_secret:
        print('❌ EPO credentials not found')
        return
    
    # Auth
    credentials = f'{consumer_key}:{consumer_secret}'
    auth = base64.b64encode(credentials.encode()).decode()
    
    ep_number = 'EP0683520'
    output_filename = f'{ep_number}_data.json'

    try:
        # follow_redirects=True rieši problém 303.
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            
            # 1. Get token
            print('\n🔑 Getting EPO token...')
            token_resp = await client.post(
                'https://ops.epo.org/3.2/auth/accesstoken', 
                headers={
                    'Authorization': f'Basic {auth}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={'grant_type': 'client_credentials'}
            )
            
            print(f"Token response status: {token_resp.status_code}")
            
            if token_resp.status_code != 200:
                print(f"❌ Token error: {token_resp.text}")
                print("\n⚠️ CHYBA: Status 401 (ClientId is Invalid). Prosím, skontrolujte platnosť kľúčov v súbore .env alebo vygenerujte nové kľúče.")
                return
                
            token = token_resp.json()['access_token']
            print('✅ Token obtained')
            
            # 2. Fetch patent data
            print(f'\n📡 Fetching patent {ep_number}...')
            
            resp = await client.get(
                f'https://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/{ep_number}',
                headers={
                    'Authorization': f'Bearer {token}',
                    'Accept': 'application/json'
                }
            )
            
            print(f"Patent response status: {resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()

                # Uloženie celého JSON do súboru
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f'\n💾 Údaje uložené do súboru: {output_filename}')
                
                # Extrakcia a výpočet (teraz by mala fungovať správne)
                dates = get_patent_dates(data)
                expiration_date = calculate_theoretical_expiration(dates['application_date'])

                # VÝSTUP VO FORME PREHĽADNEJ TABUĽKY
                print('\n======================================================')
                print(f'         📊 Prehľad EPO Patentu {ep_number}          ')
                print('======================================================')
                print(f'| Dátum podania prihlášky (Application Date):  {dates["application_date"]} |')
                print(f'| Dátum udelenia patentu (Grant Date):          {dates["grant_date"]} |')
                print('------------------------------------------------------')
                print('| Teoretická MAXIMÁLNA exspirácia (20 rokov):         |')
                print(f'| Dátum: {expiration_date}                          |')
                print('======================================================')
                print('\n⚠️ POZNÁMKA: Pre zistenie skutočného stavu (či neboli')
                print('zapreté poplatky) je nutný dopyt na Legal Status API.')
                
            else:
                print(f"❌ Chyba: {resp.text}")
                
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_epo())