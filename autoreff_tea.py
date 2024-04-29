from seleniumbase import SB
import time
import csv
import names
import random
import string

def extract_email_password(csv_file):
    emails_passwords = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:  # Assuming email is in first column and password in second
                email = row[0]
                password = row[1]
                emails_passwords.append((email, password))
    return emails_passwords

csv_file = 'emails_tea.csv'
emails_passwords = extract_email_password(csv_file)

list_email_error = []

for email, password in emails_passwords:
    with SB(uc=True, headed=True) as driver:
        try:
            print(f"Email: {email}, Password: {password}")

            driver.get("https://accounts.google.com/signin")
            driver.type("#identifierId", email)
            driver.click("#identifierNext > div > button")

            driver.sleep(1)

            checkPassword = driver.is_element_present("#password")
            if(not checkPassword):
                driver.refresh()
                driver.sleep(1)

                driver.type("#identifierId", email)
                driver.click("#identifierNext > div > button")

                driver.sleep(1)

            driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", password)
            driver.click("#passwordNext > div > button")
            
            driver.sleep(10) 
            url ="<Reff Link In Here>" # Ganti Reff Kalian 
            driver.get(url)
            driver.sleep(1)

            driver.click('[aria-label="Launch the app with Google"]')
            driver.sleep(3)

            # Change Window Sign In
            driver.switch_to_newest_window()

            identifierCheck = '[data-identifier="' + email + '"]'
            driver.click(identifierCheck)
            driver.sleep(1)
            driver.click('button:contains("Continue")')
            driver.sleep(10)

            driver.switch_to_default_window()
            driver.sleep(10)

            # checkErrorSignIn = driver.is_text_visible("Oops, could not authenticate. Refresh and try again!")
            checkAttribute = driver.is_element_present('input[name="username"]')
            if(not checkAttribute):
                driver.refresh()
                driver.sleep(3)

                driver.click('[aria-label="Launch the app with Google"]')
                driver.sleep(3)

                # Change Window Sign In
                driver.switch_to_newest_window()

                identifierCheck = '[data-identifier="' + email + '"]'
                driver.click(identifierCheck)
                driver.sleep(1)
                driver.click('button:contains("Continue")')
                driver.sleep(10)

                driver.switch_to_default_window()
                driver.sleep(1)

            name = names.get_full_name().replace(" ", "").lower() + names.get_last_name().lower()
            driver.type('[name="username"]', name)
            driver.sleep(1)

            driver.click('.text-2xl')
            driver.sleep(1)

            driver.wait_for_element_present("p.text-green-400", timeout=15)
            driver.sleep(1)
           

            driver.click('button:contains("Complete Registration")')
            driver.sleep(15)
        except Exception as e:
            print("This Email Have Exception ", email)
            list_email_error.append((email,password))
            
            
        time.sleep(3)

# Function to generate a random filename
def generate_random_filename(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length)) + '.csv'

filename = "error_email_".generate_random_filename()

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['email', 'pass'])  # Write header
    csvwriter.writerows(list_email_error)  # Write data