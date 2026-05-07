# Integrare Hydrokov pentru Home Assistant

Această integrare permite citirea datelor de la portalul client **Hydrokov** (România) direct în Home Assistant.

## Funcționalități

- Index contor apă curent (m³)
- Ultimul consum (m³)
- Data ultimei citiri
- Valoarea ultimei facturi (RON)
- Suma de plătit (RON)
- Număr total facturi
- Ultimele **6 indexuri** ale contorului (în atribute)
- Ultimele **6 facturi** detaliate (în atribute)

## Instalare

### 1. Prin HACS (recomandat)

1. Deschide HACS
2. Mergi la **Integrations**
3. Apasă **Explore & Download Repositories**
4. Caută: `Hydrokov`
5. Instalează și restartează Home Assistant

### 2. Instalare manuală

1. Copiază folderul `hydrokov` în `/config/custom_components/`
2. Restartează Home Assistant
3. Mergi la **Setări → Dispozitive și servicii → Adaugă integrare**
4. Caută: **Hydrokov**

## Configurare

La adăugarea integrării completează:

- **Email**: adresa cu care te autentifici pe [app.hydrokov.ro](https://app.hydrokov.ro)
- **Parolă**: parola contului
- **Client ID**: apare pe ultima factura (sau verifică pe portal)

## Entități disponibile

| Nume entitate                    | Tip       | Descriere                          |
|----------------------------------|-----------|------------------------------------|
| Vízmérő állás                    | Sensor    | Index contor actual (m³)           |
| Legutóbbi fogyasztás             | Sensor    | Ultimul consum                     |
| Utolsó leolvasás                 | Sensor    | Data ultimei citiri                |
| Legutóbbi számla                 | Sensor    | Valoarea ultimei facturi           |
| Fizetendő összeg                 | Sensor    | Sumă de plătit                     |
| Összes számla száma              | Sensor    | Număr total facturi                |

**Atribute** (când apeși pe entitate):
- `allás_1` … `allás_6` → ultimele indexuri cu dată
- `szamla_1` … `szamla_6` → ultimele facturi detaliate

## Logo

Poți adăuga logo-ul în fișierul `icons/hydrokov.png` (recomandat 512×512 px).

## Depanare

- Dacă nu se încarcă datele → verifică jurnalele (caută `hydrokov`)
- La erori de autentificare integrarea încearcă automat reconectarea

---

**Versiune:** 1.0.0  
**Realizat:** konczei.lehel@gmail.con (2026)