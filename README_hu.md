# Hydrokov Integráció Home Assistant-hez

Ez az integráció lehetővé teszi a **Hydrokov SA** (Kovászna megyei vízszolgáltató) ügyfélportáljának adatainak lekérését közvetlenül a Home Assistant-be.

## Funkciók

- Jelenlegi vízóra állás (m³)
- Legutóbbi fogyasztás (m³)
- Utolsó leolvasás dátuma
- Legutóbbi számla összege (RON)
- Fizetendő összeg (RON)
- Összes számla száma
- Utolsó **8 vízóra állás** (attribútumokban)
- Utolsó **6 számla** részletesen (attribútumokban)

## Telepítés

### 1. HACS-szal (ajánlott)

1. Nyisd meg a HACS-t → **Integrations**
2. Kattints a **Explore & Download Repositories** gombra
3. Keresd: `Hydrokov`
4. Telepítsd és indítsd újra a Home Assistant-ot

### 2. Manuális telepítés

1. Másold a `hydrokov` mappát a `/config/custom_components/` könyvtárba
2. Indítsd újra a Home Assistant-ot
3. Menj **Beállítások → Eszközök és szolgáltatások → Integráció hozzáadása**
4. Keresd és add hozzá: **Hydrokov**

## Beállítás

Az integráció hozzáadásakor add meg:

- **Email**: az [app.hydrokov.ro](https://app.hydrokov.ro) oldalon használt email címed
- **Jelszó**: a fiókod jelszava
- **Client ID**: általában `TSY4647`

## Elérhető entitások

| Entitás neve                  | Típus     | Leírás                              |
|-------------------------------|-----------|-------------------------------------|
| Water Meter Reading           | Sensor    | Jelenlegi vízóra állás (m³)         |
| Latest Consumption            | Sensor    | Legutóbbi fogyasztás (m³)           |
| Last Reading Date             | Sensor    | Utolsó leolvasás dátuma             |
| Latest Invoice                | Sensor    | Legutóbbi számla összege (RON)      |
| Outstanding Amount            | Sensor    | Fizetendő összeg                    |
| Total Invoices                | Sensor    | Összes számla száma                 |

### Hasznos attribútumok

**Water Meter Reading** (fő vízóra entitás):
- `reading_1` → `reading_8`: utolsó vízóra állások dátummal

**Latest Invoice** (fő számla entitás):
- `invoice_1` → `invoice_6`: utolsó számlák részletei
- `invoices_count`: összes számla száma

## Depanálás (hibaelhárítás)

- Ha nem töltődnek be az adatok → ellenőrizd a naplókat (`hydrokov` kulcsszóval)
- Az integráció automatikusan újra bejelentkezik hibás token esetén

---

**Verzió:** 1.0.0  
**Dátum:** 2026. május  
**Készítette:** @lehel67 (konczei.lehel@gmail.com)
