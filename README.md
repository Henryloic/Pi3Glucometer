# 📈 Glucose Dashboard Raspberry Pi

Dashboard glycémie temps réel basé sur LibreLinkUp, développé en Python avec Flask pour Raspberry Pi.

L'application récupère les mesures FreeStyle Libre via l'API LibreLinkUp et les affiche sur une interface web optimisée pour un écran dédié.

---

# ✨ Fonctionnalités

✅ Valeur glycémie temps réel

✅ Tendance glycémique

✅ Historique graphique

✅ Zones de référence :
- 70 mg/dL
- 100 mg/dL
- 180 mg/dL

✅ Couleurs automatiques :
- Vert = plage normale
- Rouge = hypo
- Orange = hyper

✅ Horloge système synchronisée NTP

✅ Clignotement intelligent :
- Lent si glycémie < 120 mg/dL et tendance baissière
- Rapide si glycémie < 80 mg/dL et tendance baissière

✅ Anti-plantage réseau

✅ Reconnexion automatique LibreLinkUp

✅ Mode OFFLINE si perte de connexion

✅ Compatible :
- Raspberry Pi Zero W
- Raspberry Pi Zero 2W
- Raspberry Pi 3B+
- Raspberry Pi 4

---

# 🖥️ Aperçu

Le dashboard est optimisé pour un affichage permanent sur écran HDMI.

Disposition :

```text
┌────────────────────┬─────────────────────┐
│      Glycémie      │       Horloge       │
│        112         │        14:32        │
│         ↓          │                     │
│       08:42        │     Graphique       │
│       LIVE         │                     │
└────────────────────┴─────────────────────┘
```

---

# 🔧 Matériel nécessaire

## Raspberry Pi

- Raspberry Pi Zero W
- Raspberry Pi Zero 2W
- Raspberry Pi 3B+
- Raspberry Pi 4

## Stockage

- Carte microSD 16 Go minimum

## Réseau

- WiFi ou Ethernet

## Affichage

- Écran HDMI
- Écran tactile HDMI
- Navigateur web

---

# 💾 Installation du Raspberry Pi

## Installation de Raspberry Pi OS

Installer :

```text
Raspberry Pi OS Lite (32-bit)
```

via Raspberry Pi Imager.

Configurer :

- SSH activé
- WiFi configuré
- Nom d'hôte personnalisé (optionnel)

---

# 🔐 Connexion SSH

Connexion :

```bash
ssh pi@pi.local
```

ou

```bash
ssh pi@adresse_ip
```

---

# 🔄 Mise à jour du système

```bash
sudo apt update
sudo apt upgrade -y
```

---

# 🐍 Installation Python

```bash
sudo apt install python3-full python3-venv -y
```

---

# 📦 Création d'un environnement virtuel

Créer :

```bash
python3 -m venv glucose_env
```

Activer :

```bash
source glucose_env/bin/activate
```

Sortir :

```bash
deactivate
```

---

# 📥 Installation des dépendances

```bash
pip install flask pylibrelinkup
```

---

# ⚙️ Configuration

Dans le script :

```python
EMAIL = "votre_email"
PASSWORD = "votre_mot_de_passe"
```

Renseigner vos identifiants LibreLinkUp.

---

# ▶️ Lancement

Démarrage manuel :

```bash
python glucose_dashboard.py
```

Accès :

```text
http://pi.local:5000
```

ou

```text
http://IP_DU_PI:5000
```

---

# 🚀 Démarrage automatique (systemd)

Créer :

```bash
sudo nano /etc/systemd/system/glucose.service
```

Contenu :

```ini
[Unit]
Description=Glucose Dashboard
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi
ExecStart=/home/pi/glucose_env/bin/python /home/pi/glucose_dashboard.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activation :

```bash
sudo systemctl daemon-reload
sudo systemctl enable glucose
sudo systemctl start glucose
```

---

# 🔍 Diagnostic

État du service :

```bash
systemctl status glucose
```

Logs :

```bash
journalctl -u glucose -f
```

---

# 🕒 Vérification de l'heure système

Afficher l'heure :

```bash
date
```

Afficher l'état NTP :

```bash
timedatectl
```

Résultat attendu :

```text
System clock synchronized: yes
NTP service: active
```

Activer NTP si nécessaire :

```bash
sudo timedatectl set-ntp true
```

L'horloge affichée dans le dashboard est basée sur l'heure système du Raspberry Pi.

---

# 🛑 Arrêt sécurisé du Raspberry Pi

Toujours arrêter proprement :

```bash
sudo shutdown -h now
```

Attendre quelques secondes puis couper l'alimentation.

---

# 🏗️ Architecture logicielle

```text
LibreLinkUp
       │
       ▼
PyLibreLinkUp
       │
       ▼
Python
       │
       ▼
Flask
       │
       ▼
HTML + CSS + SVG
       │
       ▼
Navigateur Web
```

---

# 📚 Technologies utilisées

- Python 3
- Flask
- LibreLinkUp
- HTML
- CSS
- SVG
- Raspberry Pi OS

---

# ⚠️ Avertissement

Ce projet est fourni à des fins personnelles et éducatives.

Il ne remplace pas :

- l'application officielle LibreLink
- les recommandations médicales
- un dispositif médical certifié

Les décisions médicales doivent être prises à partir des dispositifs officiels et en accord avec les recommandations de santé.

---

# 👨‍💻 Auteur

Loïc Henry

Projet personnel Raspberry Pi / LibreLinkUp.
