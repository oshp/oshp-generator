# OWASP Secure Headers Project generator

The objective is to provide a way to generate the configuration for different web/app server with the headers to **add** and **remove** using the [reference json files](https://github.com/OWASP/www-project-secure-headers/tree/master/ci) provided by the OSHP project.

You can use the provided scripts, as a foundation, to tailor it to your context.

[Visual Studio Code](https://code.visualstudio.com/) is used for the tests suite development. A Visual Studio Code [workspace file](project.code-workspace) is provided for the project with [recommended extensions](.vscode/extensions.json).

# Status

![status](https://img.shields.io/badge/status-Under%20Active%20Development-informational?style=for-the-badge&logo=python)

# How to use it?

> 💻 The script does not use any external dependencies to enhance its portability.

Follow the steps below.

1. Ensure that [python3](https://www.python.org/downloads/) **>= 3.9** is installed on your platform.
2. Run the following commands corresponding to your context:

```bash
$ python --version
Python 3.9.7

$ python ./scripts/generate_config_snippet.py --help
usage: generate_config_snippet.py [-h] --server {APACHE_HTTP_SERVER,NGINX,IIS} --action {ADD,REMOVE} [--source JSON_LOCATION] [--output OUTPUT_FILE]

Script generating the configuration instructions snippet for different web/app server with the headers to ADD and REMOVE using the reference json files provided by the OSHP project

optional arguments:
  -h, --help            show this help message and exit
  --source JSON_LOCATION
                        Location where the reference json files can be found (default to GitHub OSHP OWASP repository).
  --output OUTPUT_FILE  File in which the generated content must be written (default to file 'snippet.conf' in current execution folder).

required named arguments:
  --server {APACHE_HTTP_SERVER,NGINX,IIS}
                        Name of the target server for which the configuration instructions snippet must be generated.
  --action {ADD,REMOVE}
                        Type of action performed on headers.

$ python ./scripts/generate_config_snippet.py --output ./generated/test.conf --server APACHE_HTTP_SERVER --action ADD
[+] Load JSON source from 'https://raw.githubusercontent.com/OWASP/www-project-secure-headers/master/ci'.
[+] Generate headers 'ADD' instructions for server software name 'APACHE_HTTP_SERVER'.
[+] Save generated instructions to file './generated/test.conf'.
[V] Instructions successfully generated and saved.

$ cat ./generated/test.conf
Header always set Cache-Control "no-store, max-age=0"
Header always set Clear-Site-Data "\"cache\",\"cookies\",\"storage\""
...
```

# References

* <https://httpd.apache.org/docs/2.4/mod/mod_headers.html>
* <https://github.com/openresty/headers-more-nginx-module>
* <https://redmine.lighttpd.net/projects/lighttpd/wiki/Docs_ModSetenv>
* <https://docs.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/>
* <https://blog.g3rt.nl/nginx-add_header-pitfall.html>
