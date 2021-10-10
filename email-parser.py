import os

# Typical Format of Email Header

# From MAILER-DAEMON Mon Mar  8 10:59:28 2021
# Date: 08 Mar 2021 10:59:28 -0500
# From: Mail System Internal Data <MAILER-DAEMON@monkey.org>
# Subject: DON'T DELETE THIS MESSAGE -- FOLDER INTERNAL DATA
# Message-ID: <1615219168@monkey.org>
# X-IMAP: 1615219168 0000000157
# Status: RO
# \n

def parse_email(email_file):
    # Get the input file name phishing-2020.txt
    base_file_name = email_file.split("\\")[-1][:-4]
    file = open(email_file, 'r', encoding="utf8")
    # Loop through the phishing_YYYY.txt file line by line
    count = 0
    while True:
        building_email = ''
        line = file.readline()
        # Check if the current line is From X
        if line[0:5] == 'From ':
            count += 1
            building_email += line
            # getting_header variable is used to indicate that we are currently getting a header
            getting_header = True
            while getting_header:
                next_line = file.readline()
                # If we detect a single new line character, we have moved to the email body
                if next_line == '\n':
                    getting_header = False
                    break
                # Else add the next line to the header
                else:
                    building_email += next_line
        # Email Header has been built, write it to file
        if building_email:
            print(count)
            f = open('phishing-emails/' + base_file_name + '-' + str(count) + '.txt', 'w', encoding="utf8")
            f.write(building_email)
            f.close()
        if not line:
            break
    file.close()


if __name__ == "__main__":
    # Looping Through Directory
    directory = os.getcwd() + '\phishing-compilation'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            input_file = os.path.join(directory, filename)
            parse_email(input_file)
        else:
            continue