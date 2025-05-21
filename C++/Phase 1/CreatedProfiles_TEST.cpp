#include <iostream>
#include <string>
#include "CreatedProfiles.h"

using std::cout;
using std::cin;
using std::endl;
using std::string;
using namespace KeypadController;

CreatedProfiles profileDB;  // global instance for testing

void loadProfiles(const string& path) {
    profileDB.loadFromFile(path);
    cout << "[Test] Profiles loaded.\n" << endl;
}

void showAllProfiles() {
    const auto& names = profileDB.getAllProfileNames();
    cout << "Available profiles:\n";
    for (const auto& name : names) {
        cout << " - " << name << endl;
    }
    cout << endl;
}

void getKeyMap(const string& profileName) {
    try {
        const auto& keyMap = profileDB.getKeyMap(profileName);
        cout << "Key map for profile \"" << profileName << "\":" << endl;
        for (const auto& [pos, action] : keyMap) {
            cout << "[" << pos.first << "-" << pos.second << "] "
                 << action.label << " | " << action.type << " | " << action.value << endl;
        }
        cout << endl;
    } catch (const std::out_of_range&) {
        cout << "Profile not found: " << profileName << endl;
    }
}

void getMediaData(const string& profileName) {
    try {
        const auto& media = profileDB.getMedia(profileName);
        cout << "Media info for profile \"" << profileName << "\":" << endl;
        for (const auto& [key, value] : media) {
            cout << key << ": " << value << endl;
        }
        cout << endl;
    } catch (const std::out_of_range&) {
        cout << "Profile not found: " << profileName << endl;
    }
}

int main() {
    string filePath;
    cout << "Enter path to saved_profiles.txt: ";
    getline(cin, filePath);

    loadProfiles(filePath);
    showAllProfiles();

    string selectedProfile;
    cout << "Enter profile name to inspect: ";
    getline(cin, selectedProfile);

    getKeyMap(selectedProfile);
    getMediaData(selectedProfile);

    return 0;
}
