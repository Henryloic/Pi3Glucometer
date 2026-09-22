from flask import Flask, render_template_string
from pylibrelinkup import PyLibreLinkUp
from datetime import datetime
import time
import socket   # ✅ IMPORTANT
app = Flask(__name__)
# =========================
# CONFIGURATION
# =========================
EMAIL = "xxxxxx@gmail.com"
PASSWORD = "xxxxxxxxx"
LOW_LIMIT = 70
HIGH_LIMIT = 180
TARGET_LINE = 100
CACHE_SECONDS = 60
# Anti-plantage
NETWORK_TIMEOUT = 12
MAX_RETRIES = 3
RETRY_SLEEP = 3
socket.setdefaulttimeout(NETWORK_TIMEOUT)
client = None
patient = None
last_data = {}
last_time = 0
last_error = ""
# =========================
# OUTILS
# =========================
def trend_arrow(t):
    return {
        1: "↓",
        2: "↘",
        3: "→",
        4: "↗",
        5: "↑"
    }.get(t, "?")
def value_color(value):
    if value < LOW_LIMIT:
        return "#e25c5c"
    elif value > HIGH_LIMIT:
        return "#f0a33a"
    else:
        return "#50c878"
def normalize_timestamp(ts):
    if isinstance(ts, datetime):
        return ts.strftime("%H:%M")
    return str(ts)
# ✅ Horloge système (NTP)
def get_local_time():
    return datetime.now().strftime("%H:%M")
# ✅ Gestion clignotement
def compute_blink(value, trend):
    if value < 80 and trend in ["↓", "↘"]:
        return "fast"
    if value < 120 and trend in ["↓", "↘"]:
        return "slow"
    return "none"
def reset_client():
    global client, patient
    client = None
    patient = None
def ensure_client():
    global client, patient
    if client is None:
        client = PyLibreLinkUp(email=EMAIL, password=PASSWORD)
        client.authenticate()
        patient = client.get_patients()[0]
# =========================
# SVG GRAPHIQUE (inchangé)
# =========================
def build_svg(values):
    if not values:
        return ""
    width, height = 700, 280
    values = [float(v) for v in values if v is not None]
    vmin = min(values + [LOW_LIMIT])
    vmax = max(values + [HIGH_LIMIT])
    margin = max(10, int((vmax - vmin) * 0.1))
    vmin -= margin
    vmax += margin
    def y(v):
        return int((1 - (v - vmin) / (vmax - vmin)) * height)
    pts = [(int(i * width / max(1, len(values)-1)), y(v)) for i, v in enumerate(values)]
    poly = " ".join([f"{x},{yy}" for x, yy in pts])
    return f"""
    <svg viewBox="0 0 {width} {height}">
        <polyline points="{poly}" fill="none" stroke="#ddd" stroke-width="3"/>
    </svg>
    """
# =========================
# DATA
# =========================
def fetch_data_once():
    ensure_client()
    g = client.latest(patient_identifier=patient)
    graph = client.graph(patient_identifier=patient)
    values = [m.value for m in graph if hasattr(m, "value") and m.value]
    val = int(g.value)
    trend = trend_arrow(g.trend)
    return {
        "value": val,
        "trend": trend,
        "timestamp": normalize_timestamp(getattr(g, "timestamp", "")),
        "color": value_color(val),
        "graph": build_svg(values),
        "status": "LIVE",
        "blink": compute_blink(val, trend),
        "clock": get_local_time()
    }
def fetch_data_robust():
    global last_error
    for i in range(MAX_RETRIES):
        try:
            return fetch_data_once()
        except Exception as e:
            last_error = str(e)
            reset_client()
            time.sleep(RETRY_SLEEP)
    return None
# =========================
# PAGE WEB
# =========================
@app.route("/")
def index():
    global last_data, last_time
    if not last_data or time.time() - last_time > CACHE_SECONDS:
        data = fetch_data_robust()
        if data:
            last_data = data
            last_time = time.time()
        else:
            if last_data:
                last_data["status"] = "OFFLINE"
            else:
                last_data = {
                    "value": "--",
                    "trend": "?",
                    "timestamp": "--",
                    "color": "#999",
                    "graph": "",
                    "status": "OFFLINE",
                    "blink": "none",
                    "clock": "--:--"
                }
    return render_template_string("""
<html>
<head>
<meta http-equiv="refresh" content="20">
<style>
body {
    margin:0;
    background:#111;
    color:white;
    font-family:Arial;
}
.container {
    display:flex;
    height:100vh;
}
.left {
    width:40%;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}
.value {
    font-size:110px;
    font-weight:bold;
    color: {{color}};
}
/* CLIGNOTEMENT */
@keyframes slow {
    0%{opacity:1;}
    50%{opacity:0.5;}
    100%{opacity:1;}
}
@keyframes fast {
    0%{opacity:1;}
    50%{opacity:0.2;}
    100%{opacity:1;}
}
.slow { animation: slow 2s infinite; }
.fast { animation: fast 0.8s infinite; }
.trend {
    font-size:100px;
    color: {{color}};
}
.time {
    font-size:35px;
    color:#aaa;
}
.status {
    margin-top:10px;
    color: {% if status == "LIVE" %}#50c878{% else %}#e25c5c{% endif %};
}
.right {
    width:60%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}
/* HORLOGE */
.clock {
    font-size:60px;
    margin-bottom:10px;
    color:#ddd;
    opacity:0.9;
}
</style>
</head>
<body>
<div class="container">
<div class="left">
<div class="value {% if blink=='slow' %}slow{% elif blink=='fast' %}fast{% endif %}">
{{value}}
</div>
<div class="trend">{{trend}}</div>
<div class="time">{{timestamp}}</div>
<div class="status">{{status}}</div>
</div>
<div class="right">
<div class="clock">{{clock}}</div>
{{graph|safe}}
</div>
</div>
</body>
</html>
""",
value=last_data["value"],
trend=last_data["trend"],
timestamp=last_data["timestamp"],
color=last_data["color"],
graph=last_data["graph"],
status=last_data["status"],
blink=last_data["blink"],
clock=last_data["clock"]
)
# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
