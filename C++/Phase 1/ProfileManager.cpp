#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include "KeyAction.h"
#include <CreatedProfiles.h>
#include "ProfileManager.h"
using std::cout;
using std::endl;

namespace KeypadController{

    ProfileManager::ProfileManager(CreatedProfiles& profileDatabase)
    : profilesRef(profileDatabase) {}

    std::vector<std::string> ProfileManager::getAllProfileNames() const{
        return profilesRef.getAllProfileNames();
    }

    void ProfileManager::reloadProfiles(const std::string& path){
        profilesRef.loadFromFile(path);   
    }

    void ProfileManager::setActiveProfile(const std::string& profileName) {
        // Prevent redundant switching
        if (profileName == activeProfileName) {
            profileNeedsUpdate = false;
            return;
        }

        // Check if the profile exists in the database
        const std::vector<std::string>& allProfiles = profilesRef.getAllProfileNames();
        if (std::find(allProfiles.begin(), allProfiles.end(), profileName) == allProfiles.end()) {
            std::cerr << "[ProfileManager] Profile not found: " << profileName << std::endl;
            return;
        }

        // Step 1: Unset primary flag of current profile
        if (!activeProfileName.empty()) {
            profilesRef.setPrimaryFlag(activeProfileName, false);  // Assumes this method exists
        }

        // Step 2: Set primary flag for new profile
        profilesRef.setPrimaryFlag(profileName, true);  // Assumes this method exists

        // Step 3: Update internal state
        activeProfileName = profileName;
        profileNeedsUpdate = false;

        std::cout << "[ProfileManager] Switched to profile: " << activeProfileName << std::endl;
    }

    const std::string& ProfileManager::getActiveProfileName() const{
        return activeProfileName;
    }

    const std::map<std::pair<int, int>, KeyAction>& ProfileManager::getActiveProfileKeyMap() const{

    }

    const std::map<std::string, std::string>& ProfileManager::getActiveProfileMedia() const{

    }

    bool ProfileManager::encoderProfileUpdate() const{

    }
    void ProfileManager::setUpdatedProfileName(const std::string& name){

    }

}