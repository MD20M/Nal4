# Meme Generator

Flask aplikacija za generiranje memov s tekstom na slikah.

## Uporabljene tehnologije

### Programski jezik
- **Python 3.12**

### Knjižnice
- **Flask 3.0.0** - Web okvir za backend
- **Pillow 10.1.0** - Knjižnica za obdelavo slik
- **Werkzeug 3.0.1** - WSGI utility knjižnica

## Potek obdelave

### Koraki procesiranja mema:

1. **Prejem datoteke** 
   - Uporabnik naloži sliko preko HTML obrazca (`<input type="file">`)
   - Flask sprejme datoteko preko `request.files['image']`

2. **Začasno shranjevanje**
   - Slika se shrani v mapo `uploads/` kot `temp_upload.jpg`
   - To omogoča obdelavo slike s Pillow knjižnico

3. **Obdelava slike**
   - Funkcija `add_text_to_image()` odpre sliko s `PIL.Image.open()`
   - Ustvari `ImageDraw` objekt za risanje teksta
   - Naloži DejaVu Sans Bold font (ali privzetega, če ni na voljo)
   - Izračuna pozicijo teksta (centriran na vrhu in dnu)
   - Doda tekst z belimi črkami in črno obramo (`stroke`)

4. **Generiranje rezultata**
   - Modificirana slika se shrani v pomnilnik (`BytesIO`)
   - Format: JPEG s kvaliteto 95%

5. **Vrnitev slike**
   - Flask vrne sliko direktno brskalniku s `send_file()`
   - Začasna datoteka se izbriše
   - Uporabnik vidi generirani meme in ga lahko prenese na svojo napravo

## Dockerizacija

### Struktura projekta
```
meme-generator/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── templates/
│   └── index.html
└── uploads/
    └── .gitkeep
```

### Docker ukazi

#### 1. Gradnja Docker slike
```bash
docker build -t meme-generator .
```

#### 2. Zagon kontejnerja
```bash
docker run -p 5000:5000 meme-generator
```

#### 3. Preverjanje delujočih kontejnerjev
```bash
docker ps
```

### Dostop do aplikacije
Po zagonu Docker kontejnerja je aplikacija dostopna na:
- **http://localhost:5000**
- **http://127.0.0.1:5000**

## Funkcionalnosti

 - Nalaganje slike preko spletnega vmesnika  
 - Vnos zgornjega teksta  
 - Vnos spodnjega teksta  
 - Generiranje nove slike s tekstom  
 - Prikaz generiranega mema v brskalniku  
 - Prenos generiranega mema  

## Oblikovanje teksta

- **Font:** DejaVu Sans Bold, velikost 40px
- **Barva teksta:** Bela (#FFFFFF)
- **Obroba:** Črna, 2px debela
- **Pozicija:** Zgornji tekst na vrhu, spodnji na dnu (centriran)
- **Format:** Tekst se avtomatsko pretvori v velike črke (klasičen meme stil)

## Lokalni razvoj (brez Dockerja)

```bash
pip install -r requirements.txt

python app.py
```