from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurazione delle credenziali
USERNAME = "fornari.giordano"
PASSWORD = "Giordano25!"

# Imposta il percorso del driver (modifica in base al tuo sistema)

# Inizializzazione del browser
driver = webdriver.Firefox()

try:
    # Apri Instagram
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)  # Attendi il caricamento della pagina

    # Accetta i cookie (se il pulsante è presente)
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Allow')]")
        cookie_button.click()
        print("Cookie accettati.")
        time.sleep(2)  # Aspetta che il popup scompaia
    except Exception as e:
        print("Il pulsante per i cookie non è stato trovato. Procedo comunque.")
    
    time.sleep(2)  # Attendi il caricamento della pagina

    # Trova i campi di input per username e password
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    # Inserisci le credenziali
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    # Premi "Invio" per effettuare il login
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)  # Attendi il caricamento della pagina successiva

    # Verifica se il login ha avuto successo
    if "login" not in driver.current_url:
        print("Login effettuato con successo!")
    else:
        print("Errore nel login. Controlla le credenziali.")

except Exception as e:
    print(f"Si è verificato un errore: {e}")
