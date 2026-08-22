# Grand Theft Auto VI — Discord Rich Presence (RPC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Discord](https://img.shields.io/badge/Discord-Rich_Presence-5865F2.svg?logo=discord&logoColor=white)](https://discord.com)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-informational.svg)]()

A lightweight, realistic Grand Theft Auto VI Discord Rich Presence simulator. Designed to emulate an authentic internal developer/QA playtest build running on the State of Leonida test branch.

---

## Preview & Features

- **Realistic QA & Playtest Simulation**: Displays authentic build numbers, RAGE 9 engine tags, and branch identifiers (e.g. `v1.0.8492-qa (branch: leonida_rel_dvt)`).
- **Dynamic Scenario Engine**: Seamlessly rotates realistic in-game activities every few minutes:
  - **Protagonists**: Lucia Caminos, Jason Duane, and Dual Co-op campaign states.
  - **Locations**: Vice Beach (Ocean Drive), Downtown Vice City, Port Gellhorn, Grassrivers Wetlands, Sundown Key, Little Haiti, Ambrosia County, and more.
  - **Activities**: Story heists, 4/5-star police chases with SWAT response, contraband speedboat runs, safehouse weapon modding, diner robberies, and open-world cruising.
- **Custom Preset Mode**: Lock your presence to a specific custom mission, location, or character.
- **Elapsed Time Counter**: Shows live playtime duration in your Discord profile.
- **Interactive Action Buttons**: Direct links to Rockstar Games & Social Club.
- **Cross-Platform**: Works natively on Windows, macOS, and Linux with auto-reconnection and graceful exit handling.

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/iiamdark/gtavi-discord-presence.git
cd gtavi-discord-presence
```

### 2. Launch

#### On Windows:
Double-click `start.bat` or run:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### On Linux / macOS:
```bash
chmod +x start.sh
./start.sh
```

---

## Discord Developer Portal Setup (Custom Assets)

To display custom game icons and name in Discord:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and name it `Grand Theft Auto VI` (this will be the game title shown on your profile).
3. Copy the **Application ID** (Client ID) from the **General Information** page.
4. Paste your `client_id` inside `config.json`.
5. Go to **Rich Presence** > **Art Assets** in the developer portal, and upload your custom images with these exact asset keys:

| Asset Key | Suggested Image | Purpose |
| :--- | :--- | :--- |
| `gtavi_cover` | GTA VI Logo / Key Art | Large main cover art |
| `lucia_icon` | Lucia portrait | Small avatar icon |
| `jason_icon` | Jason portrait | Small avatar icon |
| `duo_icon` | Dual character banner | Small avatar icon |
| `wanted_icon` | 5-Star wanted badge | Small pursuit icon |

*(Note: Discord may take 5–10 minutes to populate newly uploaded art assets across their CDN).*

---

## Configuration (`config.json`)

```json
{
  "client_id": "YOUR_DISCORD_APPLICATION_ID",
  "mode": "dynamic",
  "update_interval_seconds": 120,
  "show_elapsed_time": true,
  "enable_debug_metrics": true,
  "build_identifier": "v1.0.8492-qa (branch: leonida_rel_dvt)",
  "buttons": [
    {
      "label": "Rockstar Games",
      "url": "https://www.rockstargames.com/VI"
    },
    {
      "label": "Social Club",
      "url": "https://socialclub.rockstargames.com"
    }
  ],
  "custom_preset": {
    "details": "Playing as Lucia Caminos",
    "state": "Exploring Vice Beach (Free Roam)",
    "large_image": "gtavi_cover",
    "large_text": "Grand Theft Auto VI - Playtest Build #8492",
    "small_image": "lucia_icon",
    "small_text": "Lucia | Level 24"
  }
}
```

### Modes
- `"dynamic"`: Automatically cycles through realistic missions, pursuits, and open-world events at the specified interval.
- `"custom"`: Statically displays the data defined under `custom_preset`.

---

## CLI Flags

You can override configuration values directly from the command line:

```bash
python main.py --mode dynamic --interval 60
python main.py --mode custom
python main.py --config my_custom_config.json
python main.py --client-id 123456789012345678
```

---

## Troubleshooting

- **"Discord desktop client is not running"**: Make sure the Discord desktop app is open and you are logged in (browser Discord does not support local RPC sockets).
- **Images not showing on Discord**: Ensure the asset key in `config.json` / `scenarios.py` matches the uploaded asset key in your Discord Developer Portal application.
- **RPC rate limits**: Discord restricts rich presence updates to once every 15 seconds. The script enforces a minimum interval of 15 seconds.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Disclaimer

This repository is an unofficial Discord Rich Presence simulator created for educational and novelty purposes. Grand Theft Auto and Rockstar Games are registered trademarks of Take-Two Interactive Software, Inc.
