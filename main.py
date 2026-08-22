#!/usr/bin/env python3
"""
GTA VI Discord Rich Presence Simulator
Author: Open Source Community
Description: Simulates an authentic GTA VI internal playtest build on Discord.
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from pypresence import Presence, DiscordNotFound, DiscordError, InvalidID
except ImportError:
    print("[ERROR] 'pypresence' library is not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

from scenarios import generate_scenario, CHARACTERS, LOCATIONS

CONFIG_FILE = "config.json"
DEFAULT_CLIENT_ID = "123456789012345678"

# Terminal Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
  ██████╗ ████████╗ █████╗     ██╗   ██╗██╗
 ██╔════╝ ╚══██╔══╝██╔══██╗    ██║   ██║██║
 ██║  ███╗   ██║   ███████║    ██║   ██║██║
 ██║   ██║   ██║   ██╔══██║    ╚██╗ ██╔╝██║
 ╚██████╔╝   ██║   ██║  ██║     ╚████╔╝ ██║
  ╚═════╝    ╚═╝   ╚═╝  ╚═╝      ╚═══╝  ╚═╝
{Colors.HEADER} [ LEONIDA INTERNAL QA & PLAYTEST HARNESS ] {Colors.RESET}
{Colors.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}
"""
    print(banner)


def load_config(config_path: str = CONFIG_FILE) -> Dict[str, Any]:
    if not os.path.exists(config_path):
        print(f"{Colors.YELLOW}[!] Configuration file '{config_path}' not found. Generating default...{Colors.RESET}")
        default_cfg = {
            "client_id": DEFAULT_CLIENT_ID,
            "mode": "dynamic",
            "update_interval_seconds": 120,
            "show_elapsed_time": True,
            "enable_debug_metrics": True,
            "build_identifier": "v1.0.8492-qa (branch: leonida_rel_dvt)",
            "buttons": [
                {"label": "Rockstar Games", "url": "https://www.rockstargames.com/VI"},
                {"label": "Social Club", "url": "https://socialclub.rockstargames.com"}
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
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_cfg, f, indent=2)
        return default_cfg

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Failed to parse {config_path}: {e}{Colors.RESET}")
        sys.exit(1)


def sanitize_buttons(raw_buttons: Optional[list]) -> Optional[list]:
    """Validates and trims buttons for Discord API specs (max 2 buttons with valid url and label)."""
    if not raw_buttons or not isinstance(raw_buttons, list):
        return None

    valid = []
    for btn in raw_buttons[:2]:
        label = btn.get("label", "").strip()
        url = btn.get("url", "").strip()
        if label and url and (url.startswith("http://") or url.startswith("https://")):
            valid.append({"label": label[:32], "url": url})

    return valid if valid else None


def connect_rpc(client_id: str, max_retries: int = 5, retry_delay: int = 4) -> Optional[Presence]:
    print(f"{Colors.BLUE}[*] Initializing Discord RPC with Client ID: {Colors.BOLD}{client_id}{Colors.RESET}")
    for attempt in range(1, max_retries + 1):
        try:
            rpc = Presence(client_id)
            rpc.connect()
            print(f"{Colors.GREEN}[+] Discord RPC successfully connected!{Colors.RESET}\n")
            return rpc
        except (DiscordNotFound, ConnectionRefusedError, FileNotFoundError):
            print(f"{Colors.YELLOW}[!] Discord desktop client is not running. Retrying ({attempt}/{max_retries})...{Colors.RESET}")
        except InvalidID:
            print(f"{Colors.RED}[ERROR] Invalid Client ID provided: '{client_id}'.{Colors.RESET}")
            print(f"{Colors.YELLOW}[i] Check your config.json or Discord Developer Portal.{Colors.RESET}")
            return None
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Connection failed: {e}{Colors.RESET}")
        
        if attempt < max_retries:
            time.sleep(retry_delay)

    print(f"{Colors.RED}[ERROR] Could not connect to Discord. Make sure Discord is open and running.{Colors.RESET}")
    return None


def run_presence(config: Dict[str, Any]):
    client_id = str(config.get("client_id", DEFAULT_CLIENT_ID)).strip()
    mode = config.get("mode", "dynamic").lower()
    interval = max(15, int(config.get("update_interval_seconds", 120)))
    show_elapsed = config.get("show_elapsed_time", True)
    build_id = config.get("build_identifier", "v1.0.8492-qa (branch: leonida_rel_dvt)")
    buttons = sanitize_buttons(config.get("buttons", []))

    start_timestamp = int(time.time()) if show_elapsed else None

    rpc = connect_rpc(client_id)
    if not rpc:
        sys.exit(1)

    print(f"{Colors.BOLD}Simulation Mode:{Colors.RESET} {Colors.GREEN}{mode.upper()}{Colors.RESET}")
    print(f"{Colors.BOLD}Update Interval:{Colors.RESET} {interval}s")
    print(f"{Colors.BOLD}Build Tag:{Colors.RESET} {build_id}")
    print(f"{Colors.DIM}Press Ctrl+C at any time to disconnect and exit.{Colors.RESET}\n")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            now_str = datetime.now().strftime("%H:%M:%S")

            if mode == "custom":
                preset = config.get("custom_preset", {})
                payload = {
                    "details": preset.get("details", "Playing GTA VI"),
                    "state": preset.get("state", "Vice City"),
                    "large_image": preset.get("large_image", "gtavi_cover"),
                    "large_text": preset.get("large_text", f"GTA VI ({build_id})"),
                    "small_image": preset.get("small_image", "lucia_icon"),
                    "small_text": preset.get("small_text", "Lucia"),
                }
            else:
                # Dynamic mode
                payload = generate_scenario(custom_build_tag=build_id)

            # Build kwargs for pypresence
            kwargs = {
                "details": payload["details"],
                "state": payload["state"],
                "large_image": payload["large_image"],
                "large_text": payload["large_text"],
                "small_image": payload["small_image"],
                "small_text": payload["small_text"],
            }

            if start_timestamp:
                kwargs["start"] = start_timestamp

            if buttons:
                kwargs["buttons"] = buttons

            rpc.update(**kwargs)

            print(f"[{Colors.CYAN}{now_str}{Colors.RESET}] {Colors.GREEN}Presence Updated (Cycle #{cycle_count}):{Colors.RESET}")
            print(f"  {Colors.BOLD}Activity:{Colors.RESET}  {payload['details']}")
            print(f"  {Colors.BOLD}State:{Colors.RESET}     {payload['state']}")
            print(f"  {Colors.BOLD}Build:{Colors.RESET}     {payload['large_text']}")
            print(f"  {Colors.DIM}------------------------------------------------------------{Colors.RESET}")

            if mode == "custom":
                # For custom mode, we can sleep indefinitely in increments until interrupted
                time.sleep(interval)
            else:
                time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Shutting down presence and disconnecting from Discord...{Colors.RESET}")
        try:
            rpc.clear()
            rpc.close()
        except Exception:
            pass
        print(f"{Colors.GREEN}[+] Clean exit. Happy testing!{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Grand Theft Auto VI - Discord Rich Presence Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-c", "--config", default=CONFIG_FILE, help="Path to config.json file")
    parser.add_argument("-m", "--mode", choices=["dynamic", "custom"], help="Override simulation mode")
    parser.add_argument("-i", "--interval", type=int, help="Override rotation interval in seconds")
    parser.add_argument("--client-id", type=str, help="Override Discord Application Client ID")

    args = parser.parse_args()

    # Enable ANSI escape sequences on Windows terminals
    if os.name == 'nt':
        os.system('')

    clear_screen()
    print_banner()

    config = load_config(args.config)

    if args.mode:
        config["mode"] = args.mode
    if args.interval:
        config["update_interval_seconds"] = args.interval
    if args.client_id:
        config["client_id"] = args.client_id

    run_presence(config)


if __name__ == "__main__":
    main()
