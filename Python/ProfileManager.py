import os
import json

class ProfileManager:
    def __init__(self, profile_file="saved_profiles.txt"):
        self.profile_file = profile_file     # Where profiles are saved
        self.profiles = {}                   # Loaded profile data
        self.current_profile_name = None     # Active profile name
        
        #self.check_doc_status()
        self.load_profiles()

    def save_profiles(self, profile_name):
        if profile_name == "__DEFAULT PROFILE__":
            # Positional key structure: "row-col"
            # default_file_path = ""
            default_keys = {
                "0-0": {"LABEL": "⎋", "TYPE": "keycode", "VALUE": "Escape"},
                "0-1": {"LABEL": "/", "TYPE": "character", "VALUE": "/"},
                "0-2": {"LABEL": "*", "TYPE": "character", "VALUE": "*"},
                "0-3": {"LABEL": "-", "TYPE": "character", "VALUE": "-"},
                "0-4": {"LABEL": "¥", "TYPE": "character", "VALUE": "¥"},

                "1-0": {"LABEL": "7", "TYPE": "character", "VALUE": "7"},
                "1-1": {"LABEL": "8", "TYPE": "character", "VALUE": "8"},
                "1-2": {"LABEL": "9", "TYPE": "character", "VALUE": "9"},
                "1-3": {"LABEL": "+", "TYPE": "character", "VALUE": "+"},
                "1-4": {"LABEL": "£", "TYPE": "character", "VALUE": "£"},

                "2-0": {"LABEL": "4", "TYPE": "character", "VALUE": "4"},
                "2-1": {"LABEL": "5", "TYPE": "character", "VALUE": "5"},
                "2-2": {"LABEL": "6", "TYPE": "character", "VALUE": "6"},
                # 2-3 is missing intentionally
                "2-4": {"LABEL": "δ", "TYPE": "keycode", "VALUE": "δ"},

                "3-0": {"LABEL": "1", "TYPE": "character", "VALUE": "1"},
                "3-1": {"LABEL": "2", "TYPE": "character", "VALUE": "2"},
                "3-2": {"LABEL": "3", "TYPE": "character", "VALUE": "3"},
                "3-3": {"LABEL": "↩", "TYPE": "character", "VALUE": "Enter"},
                "3-4": {"LABEL": "©", "TYPE": "character", "VALUE": "©"},

                "4-0": {"LABEL": "0", "TYPE": "character", "VALUE": "0"},
                "4-2": {"LABEL": ".", "TYPE": "character", "VALUE": "."},
                "4-4": {"LABEL": "€", "TYPE": "character", "VALUE": "€"}
            }

            blank_media = {
                "TYPE": "None",
                "VALUE": "empty"
            }

            self.profiles["Default"] = {
                "name": "Default",
                "keys": default_keys,
                "media": blank_media,
                "primary": True
            }

        else:
            # Create a blank profile but with correct positions
            default_positions = [
                "0-0", "0-1", "0-2", "0-3", "0-4",
                "1-0", "1-1", "1-2", "1-3", "1-4",
                "2-0", "2-1", "2-2", "2-4",   # Skip 2-3
                "3-0", "3-1", "3-2", "3-3", "3-4",
                "4-0", "4-2", "4-4"           # Skip 4-1, 4-3
            ]
            labels = [
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10",
                "11", "12", "13", "14",
                "15", "16", "17", "18", "19",
                "20", "21", "22"
            ]

            blank_keys = {}
            for pos, label in zip(default_positions, labels):
                blank_keys[pos] = {
                    "LABEL": label,
                    "TYPE": "character",
                    "VALUE": label
                }
            blank_media = {
                "TYPE": "None",
                "VALUE": "Empty"
            }

            self.profiles[profile_name] = {
                "name": profile_name,
                "media":blank_media,
                "keys": blank_keys,
                "primary": False
            }

        self._write_to_file()


    def _write_to_file(self):
        with open(self.profile_file, "w") as f:
            json.dump(self.profiles, f, indent=4)

    def load_profiles(self):
        if not os.path.exists(self.profile_file):
            print("Profile file not found. Creating default.")
            self.save_profiles("__DEFAULT PROFILE__")
            # After creating, reload it!
        
        try:
            with open(self.profile_file, "r") as f:
                self.profiles = json.load(f)
        except Exception as e:
            print(f"Error loading profiles: {e}")
            self.save_profiles("__DEFAULT PROFILE__")
            # Try loading again after fixing
            with open(self.profile_file, "r") as f:
                self.profiles = json.load(f)

        # Try to find the profile with primary = True
        primary_found = False
        for name, profile in self.profiles.items():
            if profile.get("primary", False):
                self.current_profile_name = name
                primary_found = True
                break

        # Fallback to first profile if no primary found
        if not primary_found and self.profiles:
            first_profile = next(iter(self.profiles))
            self.current_profile_name = first_profile
            self.profiles[first_profile]["primary"] = True
            self._write_to_file()

    def get_current_profile(self):
        return self.profiles.get(self.current_profile_name)

    def add_profiles(self, profile_name):
        if profile_name in self.profiles:
            print(f"Profile '{profile_name}' already exists.")
            return False

        self.save_profiles(profile_name)
        return True

    def delete_profile(self, profile_name):
        if profile_name in self.profiles:
            del self.profiles[profile_name]
            if self.current_profile_name == profile_name:
                self.current_profile_name = next(iter(self.profiles), None)
            self._write_to_file()
            return True
        return False

    def switch_profile(self, name):
        if name in self.profiles:
            for p in self.profiles.values():
                p["primary"] = False
            self.profiles[name]["primary"] = True
            self.current_profile_name = name
            self._write_to_file()
            return True
        return False

    def get_profile_names(self):
        return list(self.profiles.keys())
