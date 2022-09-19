#!/usr/bin/python3
"""
Script generating the configuration instructions snippet for different web/app server with the headers 
to ADD and REMOVE using the reference json files provided by the OSHP project:

    https://github.com/OWASP/www-project-secure-headers/tree/master/ci

Sources:
    https://httpd.apache.org/docs/2.4/mod/mod_headers.html
    https://github.com/openresty/headers-more-nginx-module
    https://redmine.lighttpd.net/projects/lighttpd/wiki/Docs_ModSetenv
    https://docs.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/


Extra sources:
    https://blog.g3rt.nl/nginx-add_header-pitfall.html

Notes:
    No configuration was found to remove headers from LighHttpD server.

Dependencies:
    None to enhance its portability
"""
import argparse
import urllib.request
import json

# Constants
DEFAULT_ENCODING = "utf-8"

# Supported server list
SUPPORTED_SERVERS = ["APACHE_HTTP_SERVER", "NGINX", "IIS"]

# Instructions templates
HEADER_ADD_APACHE_HTTP_SERVER = 'Header always set %s "%s"'
HEADER_REMOVE_APACHE_HTTP_SERVER = 'Header unset %s'
HEADER_ADD_NGINX = 'more_set_headers %s;'
HEADER_REMOVE_NGINX = 'more_clear_headers %s;'
HEADER_ADD_IIS = '<add name="%s" value="%s" />'
HEADER_REMOVE_IIS = '<remove name="%s" />'


def display_msg(message):
    """Print a message: Used as abstraction for further rendering enhancement."""
    print(message)


def get_double_quotes_escaped(string_to_escape):
    """Return a string in which the double quotes are escaped."""
    return string_to_escape.replace('"', '\\\"')


def load_json_source(action, location):
    """Load the reference json file content from the specified location whatever the location specified is local or remote."""
    target_location = f"{location}/headers_{action.lower()}.json"
    if target_location.startswith("https:"):
        config_string = urllib.request.urlopen(target_location).read().decode(DEFAULT_ENCODING)
    else:
        with open(target_location, mode="r", encoding=DEFAULT_ENCODING) as f:
            config_string = f.read()
    return json.loads(config_string)


def generate_add_instructions(server, json_source):
    """Generate the collections of instructions to add HTTP security response headers for the target server."""
    instructions = []
    if server in ["APACHE_HTTP_SERVER", "IIS"]:
        for header in json_source["headers"]:
            value = get_double_quotes_escaped(header['value'])
            if server == "APACHE_HTTP_SERVER":
                instructions.append(HEADER_ADD_APACHE_HTTP_SERVER % (header["name"], value))
            else:
                instructions.append(HEADER_ADD_IIS % (header["name"], value))
    elif server == "NGINX":
        values = ""
        for header in json_source["headers"]:
            value = get_double_quotes_escaped(header['value'])
            values += f"\"{header['name']}: {value}\" "
        instructions.append(HEADER_ADD_NGINX % values)
    return instructions


def generate_remove_instructions(server, json_source):
    """Generate the collections of instructions to remove HTTP response headers for the target server."""
    instructions = []
    if server in ["APACHE_HTTP_SERVER", "IIS"]:
        for header_name in json_source["headers"]:
            if server == "APACHE_HTTP_SERVER":
                instructions.append(HEADER_REMOVE_APACHE_HTTP_SERVER % (header_name))
            else:
                instructions.append(HEADER_REMOVE_IIS % (header_name))
    elif server == "NGINX":
        instructions.append(HEADER_REMOVE_NGINX % " ".join(json_source["headers"]))
    return instructions


def save_instructions(instructions, output_file):
    """Save the collections of HTTP response headers instructions to the specified file."""
    instructions.sort()
    with open(output_file, mode="w", encoding=DEFAULT_ENCODING) as f:
        f.write("\n".join(instructions))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script generating the configuration instructions snippet for different web/app server with the headers to ADD and REMOVE using the reference json files provided by the OSHP project")
    required_params = parser.add_argument_group("required named arguments")
    required_params.add_argument("--server", action="store", dest="server_software_name",
                                 help="Name of the target server for which the configuration instructions snippet must be generated.", choices=SUPPORTED_SERVERS, required=True)
    required_params.add_argument("--action", action="store", dest="instruction_type", help="Type of action performed on headers.", choices=["ADD", "REMOVE"], required=True)
    parser.add_argument("--source", action="store", dest="json_location", help="Location where the reference json files can be found (default to GitHub OSHP OWASP repository).",
                        required=False, default="https://raw.githubusercontent.com/OWASP/www-project-secure-headers/master/ci")
    parser.add_argument("--output", action="store", dest="output_file",
                        help="File in which the generated content must be written (default to file 'snippet.conf' in current execution folder).", required=False, default="snippet.conf")
    args = parser.parse_args()
    location = args.json_location
    action = args.instruction_type
    server = args.server_software_name
    output_file = args.output_file
    display_msg(f"[+] Load JSON source from '{location}'.")
    json_source = load_json_source(action, location)
    display_msg(f"[+] Generate headers '{action }' instructions for server software name '{server}'.")
    if action == "ADD":
        instructions = generate_add_instructions(server, json_source)
    else:
        instructions = generate_remove_instructions(server, json_source)
    display_msg(f"[+] Save generated instructions to file '{output_file}'.")
    save_instructions(instructions, output_file)
    display_msg("[V] Instructions successfully generated and saved.")
