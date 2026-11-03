# Lipu Viktoriin 

Lihtne ja lõbus Pythoni ning Tkinteri abil loodud graafiline viktoriinimäng, kus mängija peab pildi järgi ära tundma riikide lipud.

---

##  Kirjeldus

Mäng valib juhuslikult riigi, laeb internetist vastava riigilipu pildi ja palub kasutajal sisestada riigi nime. Mäng arvestab punkte ja hoiab meeles parimat tulemust (rekordit).

### Mängureeglid:
* **Õige vastus:** Saad 1 punkti ja liigud järgmise lipu juurde.
* **Vale vastus:** Sul on iga lipu ära arvamiseks **5 katset**.
* **Mängu lõpp / Nullimine:** Kui eksid 5 korda järjest ühe lipu puhul, nullitakse sinu praegune punktisumma ja näidatakse õiget vastust.

---

## Nõuded ja sõltuvused

Mängu käivitamiseks on vajalik **Python 3.x** ning järgmised teegid:

* `Pillow` (piltide töötlemiseks)
* `requests` (lippude allalaadimiseks veebist)

Samuti peab projektis olema fail `andmed.py`, mis sisaldab riikide andmeid (nimesid ja koode).
