# Eesti tõenäosusskaala

Projekt visualiseerib erinevate sündmuste tõenäosusi Eestis,
aidates lugejal arendada intuitsiooni tõenäosuste kohta.

![Tõenäosusskaala](output/probability_scale.png)

## Idee

Inimestel on hea intuitsioon vahemaade kohta, kuid mitte tõenäosuste kohta.
Mis sündmused juhtuvad tõenäosusega 0.4? Mis tõenäosusega 0.0002?
See projekt vastab neile küsimustele Eesti metsa- ja rahvastikuandmete põhjal.

## Andmeallikad

Kõik andmed on laetud programmiliselt [Statistikaameti API](https://andmed.stat.ee/api/v1/et/stat) kaudu:

| Tabel | Kirjeldus |
|---|---|
| KK51.PX | Metsavaru riikliku metsainventeerimise hinnangul, 1999–2024 |
| KK513.PX | Hukkunud puistud maakonna järgi, 1991–2024 |
| RV104.PX | Sünnituste arv ja mitmikesünnitused, 1922–2024 |
| RV40.PX | Surnud surmakuu järgi, 1927–2024 |

## Tulemused

| Sündmus | Tõenäosus |
|---|---|
| Juhuslik Eesti hektar on metsamaa | 0.5198 |
| Juhuslik metsahektar on männik või kuusik | 0.4292 |
| Juhuslik metsahektar on kaasik | 0.2743 |
| Juhuslik metsahektar on haavikut | 0.0608 |
| Juhuslik sünd on kaksikud | 0.0302 |
| Juhuslik eestlane suri sel aastal | 0.0115 |
| Juhuslik metsahektar hukkub tulekahjus sel aastal | 0.000238 |

## Projekti struktuur

rmk-probability-scale/
├── src/
│   ├── fetch_data.py      # API päringud statistikaametist
│   ├── compute_probs.py   # Tõenäosuste arvutamine
│   └── visualize.py       # Graafiku genereerimine
├── output/
│   └── probability_scale.png
├── requirements.txt
└── README.md

## Käivitamine

```bash
git clone https://github.com/sifux5/rmk-probability-scale
cd rmk-probability-scale
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/visualize.py
```

Graafik salvestatakse `output/probability_scale.png`.

## Litsents

MIT