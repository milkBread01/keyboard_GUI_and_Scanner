#pragma once
#include <iostream>
#include <chrono>

namespace KeypadController {

    // Detects encoder interactions: rotation, short click, long click, and combo click.
    class Encoder {
    public:
        Encoder();

        // Polls encoder input state and updates internal tracking
        void updateState();

        // Returns true if encoder was rotated (used for scrolling or volume)
        bool isRotated() const;

        // Returns a number representing the encoder state:
        // 0 = rotate only, 1 = short click, 2 = long click, 3 = short+long combo
        int getClickPattern();

        // Clears click and timing state after handling
        void resetClickPattern();

    private:
        // Helpers for detecting timing
        bool detectShortClick();
        bool detectLongClick();
        bool detectComboClick();

        // Internal tracking
        int clickCount;
        bool rotated;
        bool isPressed;
        std::chrono::steady_clock::time_point pressStartTime;
        std::chrono::steady_clock::time_point lastClickTime;
    };
}
