# Eesti metsa tõenäosusskaala

Projekt visualiseerib erinevate metsaga seotud sündmuste tõenäosusi Eestis,
aidates lugejal arendada intuitsiooni tõenäosuste kohta.

![Tõenäosusskaala](output/probability_scale.png)

## Idee

Inimestel on hea intuitsioon vahemaade kohta, kuid mitte tõenäosuste kohta.
Mis sündmused juhtuvad tõenäosusega 0.4? Mis tõenäosusega 0.0002?
See projekt vastab neile küsimustele Eesti metsa andmete põhjal.

## Andmeallikad

Kõik andmed on laetud programmiliselt [Statistikaameti API](https://andmed.stat.ee/api/v1/et/stat) kaudu:

- **KK51.PX** – Metsavaru riikliku metsainventeerimise (SMI) hinnangul, 1999–2024
- **KK513.PX** – Hukkunud puistud maakonna järgi, 1991–2024

## Tulemused

| Sündmus | Tõenäosus |
|---|---|
| Juhuslik Eesti hektar on metsamaa | 0.520 |
| Juhuslik metsahektar on männik või kuusik | 0.429 |
| Juhuslik metsahektar on kaasik | 0.274 |
| Juhuslik metsahektar on haavikut | 0.061 |
| Juhuslik metsahektar hukkub tulekahjus sel aastal | 0.0002 |

## Projekti struktuur