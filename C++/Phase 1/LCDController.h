#pragma once
#include <iostream>
#include <vector>
#include <string>

namespace KeypadController {

    // Controls the LCD screen: shows media, battery %, profiles, and pairing UI.
    class LCDController {
    public:
        LCDController();

        // Displays the current battery level on the LCD
        void showBatteryPercentage();

        // Displays a scrollable list of available profiles for selection
        void showProfileSelector(const std::vector<std::string>& profiles);

        // Highlights the profile at the given index (rotary input from encoder)
        void highlightProfile(int index);

        // Confirms the profile selection and returns the selected profile name
        std::string confirmProfileSelection();

        // Displays a prompt for pairing decision and allows yes/no selection
        void showPairingPrompt();

        // Returns true if user selects “yes” to pairing, false if “no”
        bool getPairingDecision();

        // Loads and displays the media tied to the given profile (e.g. image or video)
        void showMediaForProfile(const std::string& profile);

        // Temporarily override the display with a message
        void overrideWithMessage(const std::string& msg);

    private:
        int selectedProfileIndex = 0;
        std::vector<std::string> currentProfileList;
    };
}
