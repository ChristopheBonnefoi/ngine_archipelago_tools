import re
from collections import defaultdict
import os

def parse_spoiler_log(file_path):
    player_settings = {}
    sender_data = defaultdict(lambda: defaultdict(list))
    receiver_data = defaultdict(lambda: defaultdict(list))
    player_info = {}
    entry_pattern = re.compile(r"^(.*)\((\w+)\): (.*) \((\w+)\)$")
    sphere_pattern = re.compile(r"^(\d+): \{")
    player_pattern = re.compile(r"^Player (\d+): (.+)")

    current_sphere = None
    in_playthrough = False
    current_player = None
    settings_buffer = []

    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            player_match = player_pattern.match(line)
            if player_match:
                player_number, player_name = player_match.groups()
                player_info[player_name] = f"P{player_number}_{player_name}"
                if current_player and settings_buffer:
                    player_settings[current_player] = "\n".join(settings_buffer)
                current_player = player_name
                settings_buffer = [line]
                continue

            if current_player and not in_playthrough:
                if line == "":
                    continue
                settings_buffer.append(line)

            if line.startswith("Playthrough"):
                if current_player and settings_buffer:
                    player_settings[current_player] = "\n".join(settings_buffer)
                in_playthrough = True
                continue

            if in_playthrough and sphere_pattern.match(line):
                current_sphere = sphere_pattern.match(line).group(1)
            elif in_playthrough and line == "}":
                current_sphere = None
            elif in_playthrough and current_sphere and entry_pattern.match(line):
                match = entry_pattern.match(line)
                if match:
                    check_location, sender, item, receiver = match.groups()
                    sender_data[sender][current_sphere].append(f"{check_location}({sender}): {item} ({receiver})")
                    receiver_data[receiver][current_sphere].append(f"{check_location}({sender}): {item} ({receiver})")

    return player_settings, sender_data, receiver_data, player_info

def write_logs_by_sender(player_settings, sender_data, receiver_data, player_info, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for player_name, formatted_name in player_info.items():
        file_path = os.path.join(output_dir, f"{formatted_name}_spoiler.log")

        with open(file_path, 'w', encoding="utf-8") as f:
            settings = player_settings.get(player_name, "Aucun paramètre trouvé pour ce joueur.")
            f.write(f"{settings}\n\n")

            f.write("Voici vos checks\n\n")
            if player_name in sender_data:
                for sphere, lines in sorted(sender_data[player_name].items(), key=lambda x: int(x[0])):
                    f.write(f"{sphere}:\n")
                    f.write("\n".join(lines) + "\n\n")
            else:
                f.write("Aucun item envoyé.\n\n")

            f.write("Items reçus\n\n")
            if player_name in receiver_data:
                for sphere, lines in sorted(receiver_data[player_name].items(), key=lambda x: int(x[0])):
                    f.write(f"{sphere}:\n")
                    f.write("\n".join(lines) + "\n\n")
            else:
                f.write("Aucun item reçu.\n\n")