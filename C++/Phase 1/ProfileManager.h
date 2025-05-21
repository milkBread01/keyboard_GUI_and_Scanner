#pragma once
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <utility>
#include "KeyAction.h"
#include "CreatedProfiles.h"

namespace KeypadController {

    // Manages profile selection, querying, and runtime updates
    class ProfileManager {
    public:
        ProfileManager(CreatedProfiles& profileDatabase);

        // --- From SystemManager ---
        void reloadProfiles(const std::string& path);  // Load from JSON
        void setActiveProfile(const std::string& profileName);  // Manual profile change
        const std::string& getActiveProfileName() const;

        // --- For KeyScanner ---
        const std::map<std::pair<int, int>, KeyAction>& getActiveProfileKeyMap() const;

        // --- For LCDController ---
        const std::map<std::string, std::string>& getActiveProfileMedia() const;

        // --- For Encoder ---
        bool encoderProfileUpdate() const;
        void setUpdatedProfileName(const std::string& name);

        // --- For general access ---
        std::vector<std::string> getAllProfileNames() const;

    private:
        CreatedProfiles& profilesRef;

        std::string activeProfileName;        // currently in use
        std::string updatedProfileName = "None"; // user-selected candidate
        bool profileNeedsUpdate = false;
    };
}
