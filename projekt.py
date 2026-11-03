import tkinter as tk
from random import randint
import requests
from PIL import Image, ImageTk
from andmed import riikide_koodid
from io import BytesIO

# --- Globaalsed muutujad ---
punktid = 0
punktide_max = 0
valed_katsed = 0
praegune_riik = None
lipu_foto = None


def jargmine_kusimus():
    """Valib listist uue juhusliku riigi, laeb selle lipu internetist,

    kuvab pildi aknal ja valmistab ette järgmise katse.
    """
    global valed_katsed, praegune_riik, lipu_foto

    # Nullime eelmise küsimuse valede katsete arvu ja puhastame sisestusvälja
    valed_katsed = 0
    kasutaja_vastus.delete(0, tk.END)
    tagasiside_label.config(text="")

    # Valime andmetest juhusliku riigi
    praegune_riik = riikide_koodid[randint(0, len(riikide_koodid))]
    riigi_nimi = praegune_riik["name"]
    riigi_luhend = praegune_riik["code"]

    # Moodustame lipu pildi URL-i ja laeme pildi alla
    url = f"https://flagcdn.com/w320/{riigi_luhend}.png"
    vastus = requests.get(url)

    # Muudame pildiandmed PIL (Pillow) abil Tkinterile sobivaks
    pildi_andmed = BytesIO(vastus.content)
    ava_pilt = Image.open(pildi_andmed)
    lipu_foto = ImageTk.PhotoImage(ava_pilt)

    # Kuvame lipu pildi kasutajaliideses
    lipu_label.config(image=lipu_foto, text="")

    # Abiks testimiseks: prindib konsooli õige vastuse
    print(f"Õige vastus: {riigi_nimi}")


def kontrolli_vastust(event=None):
    """Kontrollib kasutaja sisestatud vastust, haldab punkte,

    valesid katseid ja suunab õige vastuse korral järgmise küsimuseni.
    """
    global punktid, valed_katsed, punktide_max

    # Loeme kasutaja sisestuse ja eemaldame liigsed tühikud
    kasutaja_sisestus = kasutaja_vastus.get().strip()
    oige_vastus = praegune_riik["name"]

    # Võrdlemine väiketähtedena, et suured/väikesed tähed ei segaks
    if kasutaja_sisestus.lower() == oige_vastus.lower():
        # Õige vastus
        kasutaja_vastus.delete(0, tk.END)
        punktid += 1

        # Uuendame rekordit, kui praegune punktisumma on suurem
        if punktide_max < punktid:
            punktide_max = punktid
            punktide_max_label.config(text=f"Parim tulemus: {punktide_max}")

        punktide_label.config(text=f"Punktid: {punktid}")
        tagasiside_label.config(text="Õige! Tubli!", fg="green")

        # Ootame 0.5 sekundit ja liigume järgmise küsimuse juurde
        aken.after(500, jargmine_kusimus)
    else:
        # Vale vastus
        valed_katsed += 1

        if valed_katsed >= 5:
            # Kui on tehtud 5 valet katset, nullitakse punktid ja antakse õige vastus teada
            punktid = 0
            punktide_label.config(text=f"Punktid: {punktid}")
            tagasiside_label.config(text=f"5 valet katset! Õige oli: {oige_vastus}", fg="red")
            aken.after(1500, jargmine_kusimus)
        else:
            # Hoiatame kasutajat järelejäänud katsete arvust
            jaranud_katseid = 5 - valed_katsed
            tagasiside_label.config(text=f"Vale vastus! Katseid jäänud: {jaranud_katseid}", fg="orange",)
            kasutaja_vastus.delete(0, tk.END)


# --- Akna loomine ja seadistamine ---
aken = tk.Tk()
aken.title("Lipu viktoriin")
aken.geometry("550x550")

# --- GUI elementide loomine ---
punktide_max_label = tk.Label(aken, text=f"Parim tulemus: {punktide_max}", font=("Arial", 12, "bold"))
punktide_max_label.pack(pady=5)

punktide_label = tk.Label(aken, text=f"Punktid: {punktid}", font=("Arial", 12, "bold"))
punktide_label.pack(pady=5)

kusimus_label = tk.Label(aken, text="Mis riigi lipp see on?", font=("Arial", 14))
kusimus_label.pack(pady=5)

# Lipu pildi hoidmise koht
lipu_label = tk.Label(aken)
lipu_label.pack(pady=10)

# Vastuse sisestusväli
kasutaja_vastus = tk.Entry(aken, font=("Arial", 12), justify="center")
kasutaja_vastus.pack(pady=10)
# Enter-klahvi vajutus käivitab kontrolli funktsiooni
kasutaja_vastus.bind("<Return>", kontrolli_vastust)

# Kontrollimise nupp
vastamine_nupp = tk.Button(aken, text="Vasta", command=kontrolli_vastust, font=("Arial", 11), width=10)
vastamine_nupp.pack(pady=5)

# Tagasiside tekst (õige/vale teavitused)
tagasiside_label = tk.Label(aken, text="", font=("Arial", 11))
tagasiside_label.pack(pady=10)

# --- Mängu käivitamine ---
jargmine_kusimus()
aken.mainloop()