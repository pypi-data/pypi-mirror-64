# Python security.txt parser

## Install

Install from [pip](https://pypi.org/project/securitytxt-parsing/1.0/):

```
▶ pip install securitytxt-parsing==1.0
```

## Usage

Parse a `security.txt` variable:
```python3
from securitytxt import SecurityTxt

sectxt = "Contact: tom.chambaretaud@protonmail.com\nAcknowledgements: https://yeswehack.com/programs/yes-we-hack"
s = SecurityTxt()
if s.parse(sectxt):
    print("Contact : %s" % s.contact())
    print(s.to_dict()) 
```

Parse a `security.txt` URL:
```python3
from securitytxt import SecurityTxt

s = SecurityTxt()
if s.parse_url("https://securitytxt.org/.well-known/security.txt"):
    print("Contact : %s" % s.contact())
    print(s.to_dict())
```

Set `security.txt` fields :
```python3
from securitytxt import SecurityTxt

sectxt = "Contact: tom.chambaretaud@protonmail.com\nAcknowledgements: https://yeswehack.com/programs/yes-we-hack"
s = SecurityTxt(field_choices=['contact'])
if s.parse(sectxt):
    print(s.to_dict())
```
