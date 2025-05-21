#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <utility>
#include "KeyAction.h"
using std::cout;
using std::endl;
using std::string;


namespace KeypadController{
    
    // Parses the profile file into a usable nested map
    std::map<std::string, std::map<std::pair<int, int>, KeyAction>> fetchProfilesFromFile(){
        cout<<"";
    }

    // Utility to convert "row-col" string to int pair
    std::pair<int, int> parseKeyPos(const std::string& keyStr){

    }

    // Sends flags to host (e.g. profile updated)
    void sendFlag(const std::string& flagName, bool value){

    }

    // Reads flag from host (e.g. "isUpdated")
    bool readFlag(const std::string& flagName){

    }

    // Sends battery status for GUI feedback
    void sendBatteryStatus(int percentage){
        
    }

    // Sends result of pairing request
    void sendPairingStatus(bool accepted){

    }

    // Gets the filename or binary of media for a profile
    std::string getMediaForProfile(const std::string& profileName){

    }

}