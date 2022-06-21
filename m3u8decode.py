#!/bin/env python
import base64
import sys
import re

sub_chars = list("0123456789")
sub_chars_legacy = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

def progress_bar(prog=0, total=50, fin="=", unfin=" ", arrow=">"):
    prog_dis = "[{}{}{}]{}%".format(fin*prog, arrow, unfin*(total-prog-1), int((prog+1) / total*100))
    return prog_dis

def read_file(path):
    f = open(path, 'r+')
    g = open("{}.bak".format(path), 'w+')
    content = f.read()
    g.write(content)
    g.close()
    f.close()
    return content

def base64_dec_fix(data, altchars=b'+/'):
    data = bytes(data, 'utf-8')
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data).decode('utf-8')

def base64_dec_legacy(data):
    return base64.b64decode(data).decode('utf-8')

def base64_dec(data):
    try:
        return base64_dec_fix(data)
    except:
        return base64_dec_legacy(data)

def replace_string(text, r_hash, r_at, r_dollar, r_percent):
    if '#' in text:
        text = text.replace('#', r_hash)
    if '@' in text:
        text = text.replace('@', r_at)
    if '$' in text:
        text = text.replace('$', r_dollar)
    if '%' in text:
        text = text.replace('%', r_percent)
    return text

def save_to_file(text, filename):
    f=open(filename, 'w+')
    f.write(text)
    f.close()
    return 0

def opt_print(strs,switches):
    if switches == 1:
        print(strs, end="\n")
    return 0

def verify_m3u8_legacy(content):
    key_token = 0
    vid_link = 0
    if "https://app.xiaoe-tech.com/" in content:
        key_token = 1
        vid_link = 1
    return (vid_link and key_token)

def verify_m3u8(content):
    key_token = 0
    for line in content.split("\n"):
        if "#EXT-X-KEY:" in line:
            try:
                line.index("https://app.xiaoe-tech.com/get_video_key.php?edk=")
                line.index("keySource=")
                line.index("fileId=")
                line.index("3877")
                line.index("CO08TAChiaoOvUBCokYjRhNjFiNTgtMmVhNy00OWYxLTgwZGMtZTE0NTIyODc5YWIy")
                key_token = 1
            except:
                key_token = 0
                break
    return (key_token)

def known_key(filename, keys):
    keys = list(keys)
    raw_b64 = read_file(filename)
    results = base64_dec(replace_string(raw_b64, keys[0], keys[1], keys[2], keys[3]))
    if verify_m3u8(results) == 1:
        save_to_file(results, filename)
        print("[+] Done! Decrypted m3u8 file is saved in {}".format(filename))
    else:
        print(results.split("\n")[4])
        print("[-] E: No key words found, probably wrong key, please try CRACK mode.")
    return 0

def known_key_exp(filename, keys):
    keys = list(keys)
    raw_b64 = read_file(filename)
    try:
        results = base64_dec(replace_string(raw_b64, keys[0], keys[1], keys[2], keys[3]))
        if verify_m3u8(results) == 1:
            save_to_file(results, filename)
            print("[+] Done! Decrypted m3u8 file is saved in {}".format(filename))
        else:
            print(results.split("\n")[4])
            print("[-] E: No key words found, probably wrong key, please try CRACK mode.")
    except Exception as e:
        print("[-] E: {}, probably wrong key, please try CRACK mode.".format(e))
    return 0

def unknown_key(filename):
    raw_b64 = read_file(filename)
    for i in range(0, len(sub_chars)):
        for j in range(0, len(sub_chars)):
            for k in range(0, len(sub_chars)):
                for l in range(0, len(sub_chars)):
                    try:
                        results = base64_dec(replace_string(raw_b64, sub_chars[l], sub_chars[k], sub_chars[j], sub_chars[i]))
                        #print(progress_bar(i, len(sub_chars)), end="\r")
                        print("[*] Now trying #={}, @={}, $={}, %={}...".format(sub_chars[l], sub_chars[k], sub_chars[j], sub_chars[i]), end="\r")
                    except Exception as e:
                        #print(progress_bar(i, len(sub_chars)), end="\r")
                        #print("[-] E:{}, ignoring...".format(e), end="\r")
                        print("[*] Now trying #={}, @={}, $={}, %={}...".format(sub_chars[l], sub_chars[k], sub_chars[j], sub_chars[i]), end="\r")
                        continue
                    #print("[*] Verifying m3u8 file...", end="\r")
                    if verify_m3u8(results) == 1:
                        print("[+] m3u8 file verified completed.", end="\r")
                        save_to_file(results, filename)
                        print("[+] Done! Decrypted m3u8 file is saved in {}.".format(filename))
                        print("[*] Keycodes: #={}, @={}, $={}, %={}".format(sub_chars[l], sub_chars[k], sub_chars[j], sub_chars[i]))
                        sys.exit()
                    else:
                        #print(results)
                        #print("[-] m3u8 file link verified failed, continue CRACK process.", end="\r")
                        continue
    return 0

def no_args():
    file_name = input("Please input files to decode:")
    keys = input("Please input key(4 letters substitutes '#@$%', if you know):")
    if len(keys) == 4:
        known_key(file_name, keys)
    else:
        print("[*] No valid key detected, entering CRACK mode, please wait...(Don't exit this program.)")
        unknown_key(file_name)
    return 0

def hav_args(arg1, arg2):
    if arg2 != 0:
        known_key(arg1, arg2)
    else:
        unknown_key(arg1)
    return 0

def main():
    if len(sys.argv) >= 3:
        hav_args(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        print("[*] No valid key detected, entering CRACK mode, please wait...(Don't exit this program.)")
        hav_args(sys.argv[1], 0)
    else:
        no_args()

if __name__ == '__main__':
    main()
