import time
import keyboard
import pyautogui

# --- CONFIGURATION DICTIONARY ---
# The keys are trigger words. When a trigger word is detected, it will be replaced by the corresponding value.
expansions = {
    "set": "set %path% = %path%;text",
    "gcc": "gcc file -o exename",
    "sizeof int": "4",
    "sizeof char": "1",
    "sizeof float": "4",
    "sizeof double": "8",
    "size of long": "4",
    "sizeof long long": "8",
    "sizeof short": "2",
    # Espansioni per i format specifier del C:
    "format %d": "Signed decimal integer",
    "format %i": "Signed decimal integer",
    "format %u": "Unsigned decimal integer",
    "format %f": "Floating point number",
    "format %lf": "Double floating point number",
    "format %e": "Scientific notation (mantissa/exponent) using 'e' as the exponent separator",
    "format %E": "Scientific notation (mantissa/exponent) using 'E' as the exponent separator",
    "format %g": "Use %e or %f, whichever is shorter",
    "format %G": "Use %E or %f, whichever is shorter",
    "format %c": "Single character",
    "format %s": "String of characters",
    "format %p": "Pointer address in hexadecimal",
    "format %o": "Unsigned octal",
    "format %x": "Unsigned hexadecimal (lowercase)",
    "format %X": "Unsigned hexadecimal (uppercase)",
    "format %%": "Literal '%' character"
}

# --- REGISTER THE ABBREVIATIONS ---
# The keyboard.add_abbreviation() function will automatically watch for the trigger word and replace it when a separator is pressed.
for trigger, replacement in expansions.items():
    keyboard.add_abbreviation(trigger, replacement)

print("Text expander is active.")
print("Type any of the trigger words (e.g., 'hello', 'bye', 'sig') followed by a space or punctuation to expand.")
print("Press ESC to exit.")

# --- MAIN LOOP ---
# Keep the script running so that the keyboard listener stays active.
try:
    while True:
        if keyboard.is_pressed("esc"):
            print("Exiting text expander.")
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program interrupted by user.")
