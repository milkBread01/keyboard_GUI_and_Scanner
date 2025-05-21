#include <iostream>
#include <fstream>
#include <map>
#include <nlohmann/json.hpp>
#include "CreatedProfiles.h"
#include "KeyAction.h"
using std::cout;
using std::endl;
using json = nlohmann::json;
namespace KeypadController {

    void CreatedProfiles::loadFromFile(const std::string& path){
        //clear any previously saved profiles from 'profiles'
        profiles.clear();
        allProfileNames.clear();

        std::ifstream file(path);
        if(!file.is_open()){
            std::cerr<<"Failed to open file in path "<<path<<endl;
        }

        json profileJSON;
        
        try{
            file >> profileJSON;
        }catch(const std::exception& e ){
            std::cerr <<"Failed to read data from JSON file";
        }

        for(const auto& [profileName, profileData] : profileJSON.items()){
            ProfileData currentProfile;
            allProfileNames.push_back(profileName);

            for(const auto& [key_GridLocation, value_LTV] : profileData["keys"].items()){
                // keys have the format "0-1"
                size_t dashPos = key_GridLocation.find('-');
                int row = std::stoi(key_GridLocation.substr(0, dashPos));
                int col = std::stoi(key_GridLocation.substr(dashPos + 1));
                std::pair<int,int> pos = {row,col};

                KeyAction action;
                action.type = value_LTV["TYPE"];
                action.label = value_LTV["LABEL"];
                action.value = value_LTV["VALUE"];

                currentProfile.keys[pos]=action;;
            }

            for(const auto& [key, value] : profileData["media"].items()){
                if (value != "None" && value != "empty") {
                    currentProfile.media[key] = value;
                }
            }

            currentProfile.primary = profileData.value("primary", false);

            profiles[profileName] = currentProfile;
        }
    }

    const std::vector<std::string>& CreatedProfiles::getAllProfileNames() const {
        return allProfileNames;
    }

    const std::map<std::string, std::string>& CreatedProfiles::getMedia(const std::string& profileName) const{
        return profiles.at(profileName).media;
    }

    const std::map<std::pair<int, int>, KeyAction>& CreatedProfiles::getKeyMap(const std::string& profileName) const {
        return profiles.at(profileName).keys;
    }    

    void CreatedProfiles::setPrimaryFlag(const std::string& profileName, bool primaryValue){
        profiles.at(profileName).primary = primaryValue;
    }

}