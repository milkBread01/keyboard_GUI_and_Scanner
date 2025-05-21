#pragma once
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include "KeyAction.h"

namespace KeypadController{
    class CreatedProfiles {

    public:

        // Load profiles from file from local JSON file
        void loadFromFile(const std::string& path);

        // Returns the list of all profile names
        const std::vector<std::string>& getAllProfileNames() const;

        // Searches ProfileData Struct and returns the key map for a given profile
        const std::map<std::pair<int, int>, KeyAction>& getKeyMap(const std::string& profileName) const;

        // Searches ProfileData Struct and returns the media data for a given profile
        const std::map<std::string, std::string>& getMedia(const std::string& profileName) const;

        void setPrimaryFlag(const std::string& profileName, bool primaryValue);

    private:
        struct ProfileData {
            std::map<std::pair<int, int>, KeyAction> keys;
            std::map<std::string, std::string> media;
            bool primary;
        };

        std::map<std::string, ProfileData> profiles;
        std::vector<std::string> allProfileNames;
    };
}