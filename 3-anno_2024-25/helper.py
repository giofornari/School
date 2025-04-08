from pynput.keyboard import Key, Listener
import pyautogui

replacements = {
    "set": "set %path% = %path%;text",
    "gcc": "gcc file -o exename",
    "sizeof.int": "4",
    "sizeof.char": "1",
    "sizeof.float": "4",
    "sizeof.double": "8",
    "sizeof.long": "4",
    "sizeof.longlong": "8",
    "sizeof.short": "2",
    # Espansioni per i format specifier del C:
    "format-%d": "Signed decimal integer",
    "format-%i": "Signed decimal integer",
    "format-%u": "Unsigned decimal integer",
    "format-%f": "Floating point number",
    "format-%lf": "Double floating point number",
    "format-%e": "Scientific notation (mantissa/exponent) using 'e' as the exponent separator",
    "format-%E": "Scientific notation (mantissa/exponent) using 'E' as the exponent separator",
    "format-%g": "Use %e or %f, whichever is shorter",
    "format-%G": "Use %E or %f, whichever is shorter",
    "format-%c": "Single character",
    "format-%s": "String of characters",
    "format-%p": "Pointer address in hexadecimal",
    "format-%o": "Unsigned octal",
    "format-%x": "Unsigned hexadecimal (lowercase)",
    "format-%X": "Unsigned hexadecimal-(uppercase)",
    "format-%%": "Literal '%' character"
}

def on_press(key):
    global typed_keys
    global listening
    key_str = str(key).replace('\'', '')

    if key_str == macro_starter:
        typed_keys = []
        listening = True

    if listening:
        if key_str.isalpha():
            typed_keys.append(key_str)

        if key == macro_ender:
            candidate_keyword = ""
            candidate_keyword = candidate_keyword.join(typed_keys)
            if candidate_keyword != "":
                if candidate_keyword in replacements.keys():
                    pyautogui.press('backspace', presses=len(candidate_keyword)+2)
                    pyautogui.typewrite(replacements[candidate_keyword])
                    listening = False


macro_starter = '#'
macro_ender = Key.space
listening = True
typed_keys = []

with Listener(on_press=on_press) as listener:
    listener.join()
