# Hydrokov Integráció Home Assistant-hez

Ez az integráció lehetővé teszi, hogy a **Hydrokov** (Románia) vízszolgáltató ügyfélportáljáról adatokat olvass be Home Assistant-ba.

## Funkciók

- Jelenlegi vízóra állás (m³)
- Legutóbbi fogyasztás (m³)
- Utolsó leolvasás dátuma
- Legutóbbi számla összege (RON)
- Fizetendő összeg (RON)
- Összes számla száma
- Utolsó **6 vízóra állás** (attribútumokban)
- Utolsó **6 számla** részletesen (attribútumokban)

## Telepítés

### 1. HACS-szal (ajánlott)

1. Nyisd meg a HACS-t
2. Menj az **Integrations** menübe
3. Kattints a jobb felső sarokban a **Explore & Download Repositories** gombra
4. Keresd: `Hydrokov`
5. Telepítsd és indítsd újra a Home Assistant-ot

### 2. Manuális telepítés

1. Másold a `hydrokov` mappát a `/config/custom_components/` könyvtárba
2. Indítsd újra a Home Assistant-ot
3. Menj **Beállítások → Eszközök és szolgáltatások → Integráció hozzáadása**
4. Keresd meg: **Hydrokov**

## Beállítás

Az integráció hozzáadásakor add meg a következőket:

- **Email**: amivel belépsz az [app.hydrokov.ro](https://app.hydrokov.ro) oldalra
- **Jelszó**: a fiókod jelszava
- **Client ID**: általában rajta van a szamlan (ellenőrizd a portálon)

## Elérhető entitások

| Entitás neve                    | Típus     | Leírás                              |
|-------------------------------|-----------|-------------------------------------|
| Vízmérő állás                 | Sensor    | Aktuális mérőóra állás (m³)         |
| Legutóbbi fogyasztás          | Sensor    | Utolsó időszak fogyasztása          |
| Utolsó leolvasás              | Sensor    | Leolvasás dátuma                    |
| Legutóbbi számla              | Sensor    | Legutóbbi számla végösszege         |
| Fizetendő összeg              | Sensor    | Amennyit még fizetni kell           |
| Összes számla száma           | Sensor    | Darabszám                           |

**Attribútumok** (kattints az entitásra):
- `allás_1` … `allás_6` → utolsó vízóra állások dátummal
- `szamla_1` … `szamla_6` → utolsó számlák részletei

## Logo

Ha szeretnéd, tedd be a logót az `icons/hydrokov.png` fájlba (512×512 ajánlott).

## Hibaelhárítás

- Ha nem töltődnek be az adatok → nézd meg a naplókat (`hydrokov` kulcsszóval)
- Rossz jelszó vagy elavult token esetén az integráció automatikusan újra bejelentkezik
- Probléma esetén nyisd meg a naplókat és küldd el a hibát

---

**Verzió:** 1.0.0  
**Készítette:** konczei.lehel@gmail.com (2026)