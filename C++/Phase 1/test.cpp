#include <iostream>
#include <nlohmann/json.hpp>
#include <fstream>
#include <string>
using std::cout;
using std::endl;
using std::string;

int main() {
    nlohmann::json j;
    std::ifstream file("saved_profiles.txt");
    file >> j;  // This is equivalent to Python’s json.load()

    for (const auto& [profileName, profileData] : j.items()) {
        std::cout << "Profile key: " << profileName << std::endl;        

        string mediaType = profileData["media"]["TYPE"];
        string mediaContent = profileData["media"]["VALUE"];
        
        string keyContent = profileData["keys"];

        string name = profileData["name"];

        string primary = profileData["primary"];
        
        cout<<"Is Primary?: "<<primary;
        
        std::cout << "Media Type: " << mediaType << std::endl;
        std::cout << "Media Content: " << mediaContent << std::endl;

    }
    

}
