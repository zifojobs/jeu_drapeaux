"""Assemble le jeu « Trouve les drapeaux ! » en un seul fichier HTML (photos incluses).

Usage : python -I build.py   →   site/index.html
"""
import base64, io, json, pathlib
from PIL import Image

ICI = pathlib.Path(__file__).parent
PHOTOS = ICI.parent / "Semaine Sénégalaise" / "Jeu"
W, H = 720, 1280  # taille des photos WhatsApp ; toutes les coordonnées sont dans ce repère


def photo(nom):
    return Image.open(PHOTOS / f"WhatsApp Image 2026-11-01 at {nom}.jpeg").convert("RGB")


def data_url(im, q=78):
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def boites(liste):
    """(x1, y1, x2, y2) en pixels → fractions de l'image."""
    return [[round(x1 / W, 4), round(y1 / H, 4), round(x2 / W, 4), round(y2 / H, 4)] for x1, y1, x2, y2 in liste]


# Manche 1 — « Compte ! » : la photo s'affiche quelques secondes, puis on donne le nombre.
COMPTE = [
    ("19.34.12", 2, "Les caisses"),
    ("19.34.13 (5)", 3, "L'entrée"),
    ("19.34.14 (2)", 3, "Fruits et légumes"),
]

# Manche 2 — « Touche-les tous ! » : un cadre par drapeau en tissu.
TOUCHE = [
    ("19.34.13 (3)", "Les gondoles", [
        (40, 180, 180, 615), (298, 325, 385, 525), (432, 375, 505, 590),
        (495, 420, 545, 535), (555, 445, 600, 590), (595, 465, 632, 580)]),
    ("19.34.14 (1)", "L'îlot des cahiers", [
        (40, 520, 105, 680), (85, 490, 140, 580), (215, 480, 320, 720),
        (490, 520, 530, 625), (640, 510, 705, 750)]),
    ("19.34.13 (4)", "L'allée des caisses", [
        (530, 170, 715, 815), (98, 630, 135, 740), (64, 665, 85, 735), (425, 725, 445, 750)]),
]

# Manche 3 — « C'est où ? » : un zoom, quatre réponses, la première est la bonne (mélangées dans la page).
OU = [
    ("19.34.14", (140, 350, 640, 900), ["L'îlot des canettes", "La table Délia", "Les caisses", "Fruits et légumes"]),
    ("19.34.14 (3)", (300, 800, 580, 1120), ["La table Délia", "L'îlot des canettes", "L'entrée", "Les gondoles"]),
    ("19.34.13 (2)", (560, 700, 720, 1150), ["Le rayon des huiles", "La table Délia", "Les congélateurs", "Les caisses"]),
    ("19.34.13 (1)", (110, 380, 290, 600), ["L'allée « Consommons local »", "Fruits et légumes", "L'entrée", "Le rayon des huiles"]),
]

TOTAL_MAGASIN = 25  # compté sur place par Saïbo le 01/11/2026


def main():
    donnees = {
        "compte": [{"img": data_url(photo(n)), "rep": r, "lieu": l} for n, r, l in COMPTE],
        "touche": [{"img": data_url(photo(n)), "lieu": l, "boites": boites(b)} for n, l, b in TOUCHE],
        "ou": [{"zoom": data_url(photo(n).crop(c), 85), "img": data_url(photo(n)), "cadre": boites([c])[0], "choix": ch}
               for n, c, ch in OU],
        "total": TOTAL_MAGASIN,
    }
    gabarit = (ICI / "gabarit.html").read_text(encoding="utf-8")
    sortie = ICI / "site" / "index.html"  # seul le dossier site/ est publié (Vercel)
    sortie.parent.mkdir(exist_ok=True)
    sortie.write_text(gabarit.replace("/*DONNEES*/null", json.dumps(donnees, ensure_ascii=False)), encoding="utf-8")
    print(sortie, f"{sortie.stat().st_size / 1e6:.1f} Mo")


if __name__ == "__main__":
    main()
