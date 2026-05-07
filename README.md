# Integrare Hydrokov pentru Home Assistant

Această integrare permite citirea datelor din portalul client **Hydrokov SA** operator regional în judeţul Covasna direct în Home Assistant.

## Funcționalități

- Index contor apă curent (m³)
- Ultimul consum (m³)
- Data ultimei citiri
- Valoarea ultimei facturi (RON)
- Suma de plătit (RON)
- Număr total de facturi
- Ultimele **8 indexuri** ale contorului (în atribute)
- Ultimele **6 facturi** detaliate (în atribute)

## Instalare

### 1. Prin HACS (recomandat)

1. Deschide HACS → **Integrations**
2. Apasă **Explore & Download Repositories**
3. Caută: `Hydrokov`
4. Instalează și restartează Home Assistant

### 2. Instalare manuală

1. Copiază folderul `hydrokov` în `/config/custom_components/`
2. Restartează Home Assistant
3. Mergi la **Setări → Dispozitive și servicii → Adaugă integrare**
4. Caută și adaugă **Hydrokov**

## Configurare

La adăugarea integrării completează:

- **Email**: adresa de email folosită pe [app.hydrokov.ro](https://app.hydrokov.ro)
- **Parolă**: parola contului
- **Client ID**: de obicei 

## Entități disponibile

| Nume entitate                    | Tip       | Descriere                              |
|----------------------------------|-----------|----------------------------------------|
| Water Meter Reading              | Sensor    | Index contor actual (m³)               |
| Latest Consumption               | Sensor    | Ultimul consum (m³)                    |
| Last Reading Date                | Sensor    | Data ultimei citiri                    |
| Latest Invoice                   | Sensor    | Valoarea ultimei facturi (RON)         |
| Outstanding Amount               | Sensor    | Suma de plătit                         |
| Total Invoices                   | Sensor    | Număr total de facturi                 |

### Atribute utile

**Water Meter Reading** (entitate principală contor):
- `reading_1` → `reading_8`: ultimele indexuri cu dată

**Latest Invoice** (entitate principală factură):
- `invoice_1` → `invoice_6`: ultimele facturi detaliate
- `invoices_count`: număr total facturi

## Depanare

- Verifică jurnalele (caută `hydrokov`) dacă nu se încarcă datele
- Integrarea se reconectează automat la erori de autentificare

---

**Versiune:** 1.0.0  
**Data:** Mai 2026
**Realizat: ** @lehel67 (konczei.lehel@gmail.com)