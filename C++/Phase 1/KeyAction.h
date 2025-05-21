#pragma once
#include <string>

namespace KeypadController {

    // Represents a single key's mapped action within a profile
    struct KeyAction {
        std::string type;   // e.g., "character", "application", "keycode"
        std::string value;  // e.g., "A", "Escape", or path to app
        std::string label;  // Display label for UI or LCD
    };

}
