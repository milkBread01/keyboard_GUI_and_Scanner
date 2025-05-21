#pragma once
#include <iostream>
#include <string>
#include "Encoder.h"
#include "LCDController.h"
#include "ProfileManager.h"
#include "KeyScanner.h"
#include "HostCommunicator.h"

namespace KeypadController {

    // Top-level controller: coordinates Encoder, LCD, KeyScanner, HostComm, and ProfileManager.
    class SystemManager {
    public:
        SystemManager();

        // Initializes all subsystems and loads the initial profile and media
        void initialize();

        // Main loop; checks for encoder and key input, handles flags, and refreshes display if needed
        void run();

        // Responds to encoder interactions: rotation, short/long click, or combo
        void handleEncoderBehavior();

        // Handles a key press from the keypad and dispatches the associated action
        void handleKeyPress(int row, int col);

        // Refreshes the LCD to show media for the current active profile
        void updateDisplayForProfile();

        // Handles profile update from host if isUpdated flag is set
        void checkForProfileUpdates();

    private:
        Encoder encoder;
        LCDController lcd;
        ProfileManager profileManager;
        KeyScanner keyScanner;
        HostCommunicator host;

        // Tracks encoder state to distinguish short/long/combo clicks
        int encoderState = 0;

        // Utility: apply new profile system-wide
        void applyProfile(const std::string& profileName);
    };
}
