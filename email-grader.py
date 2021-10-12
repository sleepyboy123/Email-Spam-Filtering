import os
import subprocess
import csv
import re

def spam_assassin_grader(file):
    spam_process = subprocess.Popen(['spamassassin', '<', file], stdout=subprocess.PIPE)
    spam_output = spam_process.stdout.read()
    return spam_output

def spam_assassin_grade_extracter(grade):
    decoded_grade = grade.decode('utf-8')
    # Use Regex to Extract X-Spam-Level
    spam_level_group = re.search('X-Spam-Level: (.*)\n', decoded_grade)
    if spam_level_group:
        spam_level = spam_level_group.group(1)
    spam_status_group = re.search('X-Spam-Status: ([\s\S]*)autolearn=no', decoded_grade)
    # Use Regex to Extract X-Spam-Status
    if spam_status_group:
        spam_status_fields = spam_status_group.group(1)
        # Extract Values from X-Spam-Status Fields
        spam_status = spam_status_fields.split(',')[0]
        spam_score = spam_status_fields.split(',')[1][7:10]
        spam_test = spam_status_fields.split('tests')[-1][1:-1].replace("\t", "").replace("\n", "")
        return (spam_level, spam_status, spam_score, spam_test)
    else:
        return (spam_level, 'error', 'error', 'error')

def rspamc_grader(file):
    rspamc_output = subprocess.check_output(['rspamc < ' + file], shell=True)
    return rspamc_output

def rspamc_grade_extracter(grade):
    # Initialising Variables
    fields = {
        'auth_na': '',
        'date_in_past': '',
        'forged_mua_outlook': '',
        'forged_outlook_html': '',
        'forged_outlook_tags': '',
        'hfilter_hostname_unknown': '',
        'has_list_unsub': '',
        'dmarc_policy_allow': '',
        'mime_good': '',
        'mime_html_only': '',
        'missing_mid': '',
        'missing_to': '',
        'old_x_mailer': '',
        'rcvd_helo_user': '',
        'rcvd_no_tls_last': '',
        'r_no_space_in_from': '',
        'to_dn_recipients': '',
        'subj_all_caps': '',
        'r_spf_fail': '',
        'r_spf_allow': '',
        'violated_direct_spf': '',
        'whitelist_dmarc': '',
    }
    # Extract Individual Values
    decoded_grade = grade.decode('utf-8') 
    data_split = decoded_grade.split('\n')
    fields['spam'] = data_split[3]
    fields['score'] = float(data_split[4][7:-8]) - 10.00
    # Looping through all fields and adding all relevant variables
    for data in data_split:
        if 'AUTH_NA' in data:
            fields['auth_na'] = data
            continue
        if 'DATE_IN_PAST' in data:
            fields['date_in_past'] = data
            continue
        if 'FORGED_MUA_OUTLOOK' in data:
            fields['forged_mua_outlook'] = data
            continue
        if 'FORGED_OUTLOOK_HTML' in data:
            fields['forged_outlook_html'] = data
            continue
        if 'FORGED_OUTLOOK_TAGS' in data:
            fields['forged_outlook_tags'] = data
            continue
        if 'HFILTER_HOSTNAME_UNKNOWN' in data:
            fields['hfilter_hostname_unknown'] = data
            continue
        if 'HAS_LIST_UNSUB' in data:
            fields['has_list_unsub'] = data
            continue
        if 'DMARC_POLICY_ALLOW' in data:
            fields['dmarc_policy_allow'] = data
        if 'MIME_GOOD' in data:
            fields['mime_good'] = data
            continue
        if 'MIME_HTML_ONLY' in data:
            fields['mime_html_only'] = data
            continue
        if 'MISSING_MID' in data:
            fields['missing_mid'] = data
            continue
        if 'MISSING_TO' in data:
            fields['missing_to'] = data
            continue
        if 'OLD_X_MAILER' in data:
            fields['old_x_mailer'] = data
            continue
        if 'RCVD_HELO_USER' in data:
            fields['rcvd_helo_user'] = data
            continue
        if 'RCVD_HELO_USER' in data:
            fields['rcvd_helo_user'] = data
            continue
        if 'RCVD_NO_TLS_LAST' in data:
            fields['rcvd_no_tls_last'] = data
            continue
        if 'R_NO_SPACE_IN_FROM' in data:
            fields['r_no_space_in_from'] = data
            continue
        if 'TO_DN_RECIPIENTS' in data:
            fields['to_dn_recipients'] = data
            continue
        if 'SUBJ_ALL_CAPS' in data:
            fields['subj_all_caps'] = data
            continue
        if 'R_SPF_FAIL' in data:
            fields['r_spf_fail'] = data
            continue
        if 'R_SPF_ALLOW' in data:
            fields['r_spf_allow'] = data
            continue
        if 'VIOLATED_DIRECT_SPF' in data:
            fields['violated_direct_spf'] = data
            continue
        if 'WHITELIST_DMARC' in data:
            fields['whitelist_dmarc'] = data
            continue
        if 'MIME_MA_MISSING_HTML' in data:
            fields['score'] = fields['score'] - 1.00
        if 'MIME_MA_MISSING_TEXT' in data:
            fields['score'] = fields['score'] - 2.00
    return fields

if __name__ == "__main__": 
    # Initialise CSV
    results_file = open('results.csv', 'w+', newline='')
    writer = csv.writer(results_file)
    header = [
        'file name', 'X-Spam-Level', 'X-Spam-Status', 'Spam-Score', 'Spam-Test', '', 'spam', 'score',
        'auth_na', 'date_in_past', 'forged_mua_outlook', 'forged_outlook_html', 'forged_outlook_tags',
        'hfilter_hostname_unknown', 'has_list_unsub', 'dmarc_policy_allow', 'mime_good', 'mime_html_only',
        'missing_mid', 'missing_to', 'old_x_mailer', 'rcvd_helo_user', 'rcvd_no_tls_last', 'r_no_space_in_from', 
        'to_dn_recipients', 'subj_all_caps', 'r_spf_fail', 'r_spf_allow', 'violated_direct_spf', 'whitelist_dmarc'
    ]
    writer.writerow(header)
    # Looping Through Directory
    directory = os.getcwd() + '/phishing-emails'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            input_file = os.path.join(directory, filename)
            # Run Spam Assassin
            spam_assassin_grade = spam_assassin_grader(input_file)
            spam_level, spam_status, spam_score, spam_test = spam_assassin_grade_extracter(spam_assassin_grade)
            # Run RSPAMC
            rspamc_grade = rspamc_grader(input_file)
            rspamc_dict = rspamc_grade_extracter(rspamc_grade)
            # Create Dataset to be writen to CSV
            data = [
                filename, len(spam_level), spam_status, spam_score, spam_test, '', rspamc_dict['spam'], rspamc_dict['score'], 
                rspamc_dict['auth_na'], rspamc_dict['date_in_past'], rspamc_dict['forged_mua_outlook'],
                rspamc_dict['forged_outlook_html'], rspamc_dict['forged_outlook_tags'], rspamc_dict['hfilter_hostname_unknown'],
                rspamc_dict['has_list_unsub'], rspamc_dict['dmarc_policy_allow'], rspamc_dict['mime_good'], rspamc_dict['mime_html_only'], 
                rspamc_dict['missing_mid'], rspamc_dict['missing_to'], rspamc_dict['old_x_mailer'], rspamc_dict['rcvd_helo_user'], 
                rspamc_dict['rcvd_no_tls_last'], rspamc_dict['r_no_space_in_from'], rspamc_dict['to_dn_recipients'], rspamc_dict['subj_all_caps'], 
                rspamc_dict['r_spf_fail'], rspamc_dict['r_spf_allow'], rspamc_dict['violated_direct_spf'], rspamc_dict['whitelist_dmarc']
            ]
            writer.writerow(data)
        else:
            continue
    results_file.close()