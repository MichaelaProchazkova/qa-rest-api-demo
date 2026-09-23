# REST API trénink před pohovorem

Malý projekt ukazuje dvě strany REST API:

- `app.py` je jednoduchý backend ve Flasku;
- `client.py` posílá HTTP požadavky a ověřuje odpovědi.

Téma politik připomíná Safeticu, ale jde pouze o cvičnou aplikaci. Data jsou uložena jen v paměti a po restartu serveru zmizí.

## 1. Příprava prostředí na Macu nebo Linuxu

V Terminálu přejdi do složky projektu a spusť:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Aktivní virtuální prostředí poznáš podle `(.venv)` na začátku řádku.

## 2. Spuštění REST backendu

V prvním okně Terminálu spusť:

```bash
python3 app.py
```

Server poběží na adrese:

```text
http://127.0.0.1:5000
```

Toto okno nech běžet. Uvidíš v něm log každého přijatého requestu.

## 3. Otevření Swagger UI

Kdyz backend bezi, otevri v prohlizeci:

```text
http://127.0.0.1:5000/apidocs/
```

Swagger UI nacita popis z `openapi.yaml`. Rozbal endpoint, klikni na
`Try it out`, dopln vstupy a potom klikni na `Execute`. Uvidis presnou URL,
odeslany request, status code, response headers a response body.

Zkus nejdrive:

1. `GET /health`;
2. `POST /policies` s pripravenym JSON prikladem;
3. zkopiruj vracene `id`;
4. pouzij ho v `GET /policies/{policy_id}`;
5. vyzkousej neexistujici ID a sleduj status `404`.

## 4. Odeslání requestů a jejich ověření

Otevři druhé okno Terminálu, přejdi do stejné složky a spusť:

```bash
source .venv/bin/activate
python3 client.py
```

Klient postupně provede:

1. `GET /api/health` – ověří dostupnost API;
2. `POST /api/policies` – vytvoří politiku;
3. `GET /api/policies/{id}` – načte vytvořenou politiku;
4. negativní `POST` bez povinného názvu – očekává `400`;
5. `PATCH /api/policies/{id}` – politiku vypne;
6. `DELETE /api/policies/{id}` – politiku smaže;
7. opakovaný `GET` – očekává `404`.

## Co se děje v klientovi

Request:

```python
response = requests.post(
    "http://127.0.0.1:5000/api/policies",
    json={"name": "Block USB copy", "action": "block"},
    timeout=5,
)
```

Ověření status kódu:

```python
assert response.status_code == 201
```

Ověření hodnoty v JSON response:

```python
assert response.json()["action"] == "block"
```

To je základ automatizovaného API testu: **pošlu request, získám response a pomocí assertů porovnám skutečný výsledek s očekáváním**.

## Jak to popsat u pohovoru

> Připravila jsem si v Pythonu jednoduchý REST backend ve Flasku a klienta používajícího knihovnu requests. Klient posílá GET, POST, PATCH a DELETE požadavky. Ověřuji HTTP statusy i hodnoty v JSON response a mám tam také negativní scénář s chybějícím povinným polem. Prakticky jsem si tak prošla celý CRUD scénář a princip automatizované kontroly pomocí assertů.

`CRUD` znamená Create, Read, Update, Delete.

## Souvislost se Swaggerem

Swagger UI by nad stejným backendem zobrazoval dokumentaci endpointů a umožnil je ručně vyzkoušet. Tento projekt Swagger zatím nepotřebuje: endpointy volá klient přímo přes knihovnu `requests`. Postman by posílal stejné HTTP požadavky přes grafické rozhraní.

## Nejčastější problémy

### `ModuleNotFoundError`

Virtuální prostředí není aktivní nebo nejsou nainstalované závislosti:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### `Connection refused`

Backend `app.py` neběží. Spusť ho v prvním okně Terminálu.

### Port 5000 je obsazený

Na některých Macích ho může používat AirPlay Receiver. V `app.py` změň `port=5000` například na `port=5050` a stejnou změnu udělej v `BASE_URL` v souboru `client.py`.
