# Simple Home Automation Example with Wyze-SDK

Demo of [Wyze-SDK](https://github.com/shauntarves/wyze-sdk) for controlling light bulbs.

## Setup

### Credentials

To access the Wyze API, you'll need a json file named `credentials.json`, at the root of the project, with the following data:

```json
{
  "WYZE_EMAIL": "my.wyze.email@email.com",
  "WYZE_PASSWORD:"my_WAZE_passw0rd"
}
```
Note: you can add a `WYZE_TOTP_KEY` entry to bypass manual entry of 2FA code.

### Requirements

This project has two potential setups:

#### Python Poetry

Included in `pyproject.toml` and `poetry.lock` which will handle the dependencies, including unit testing and code formatting.

It is assumed that if the user is familiar with Poetry and no additional setup documentation is required.

#### Pip

Included is the `requirements.txt`. This is a trimmed down version of the project that doesn't support the code in the `tests` directory.

It is recommended that a virtual environment be used:

##### MacOS/Linux
```commandline
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip install -r requirements.txt
# ... do work
$ deactivate
# optional: $ rm -rf myenv/
```

##### Windows
```commandline
TODO
```
---
## Simple Example

From the project root, run:
```commandline
$ python3 wyze_playground/basic_menu.py
```
The following menu will appear:
```commandline
Wyze Bulb Operations:
  1) turn on bulb
  2) turn off bulb
  3) list all bulbs
  4) set bulb color
  q) quit
```
The first operation that requires an API interaction will require the 2FA used by Wyze (assuming you have 2FA set up).
```commandline
Wyze Bulb Operations:
  1) turn on bulb
  2) turn off bulb
  3) list all bulbs
  4) set bulb color
  q) quit
> 3
Enter Wyze 2FA Verification Code: 000000
'Living Room Corner', 'Bedroom Color Bulb', 'Dining Table Bulb'

Wyze Bulb Operations:
  1) turn on bulb
  2) turn off bulb
  3) list all bulbs
  4) set bulb color
  q) quit
> 1
Enter bulb name: Dining Table Bulb

Wyze Bulb Operations:
  1) turn on bulb
  2) turn off bulb
  3) list all bulbs
  4) set bulb color
  q) quit
> 4
Enter bulb name: Dining Table Bulb
Enter hex color (excluding hash): FF0000

Wyze Bulb Operations:
  1) turn on bulb
  2) turn off bulb
  3) list all bulbs
  4) set bulb color
  q) quit
> 2
Enter bulb name: Dining Table Bulb

Wyze Bulb Operations:
  1) turn on bulb
  2) turn off bulb
  3) list all bulbs
  4) set bulb color
  q) quit
> q

Process finished with exit code 0
```