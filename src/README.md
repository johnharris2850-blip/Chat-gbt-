# Source

The standalone Butano implementation lives here. `main.cpp` owns engine startup
and the top-level state transition; focused translation units own input, audio,
save data, placeholder text, and bootstrap scenes. Future systems should preserve
these boundaries rather than growing a monolithic entry point.
