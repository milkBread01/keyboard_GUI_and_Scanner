#pragma once
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include "KeyAction.h"

namespace KeypadController {

    // Scans the key matrix and dispatches actions based on the active key profile.
    class KeyScanner {
    public:
        KeyScanner();

        // Inject keymap for the currently active profile
        void setActiveKeyMap(const std::map<std::pair<int, int>, KeyAction>& keyMap);

        // Scans the matrix for a key press and determines row/col
        void scanKeys();

        // Performs an action associated with the detected key
        void performAction(const KeyAction& action);

        // Actions (called by performAction)
        void launchApp(const std::string& path);
        void openWebsite(const std::string& url);
        void sendChars(const std::string& chars);
        void executeSequence(const std::vector<std::string>& steps);

    private:
        std::map<std::pair<int, int>, KeyAction> currentKeyMap;
    };
}
