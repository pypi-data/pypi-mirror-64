from urllib.parse import urlparse
import time

import requests

FIELD_CHOICES = ["contact", "encryption", "acknowledgements", "preferred-languages", "canonical", "policy", "hiring"]

class SecurityTxt:

    def __init__(self, field_choices=FIELD_CHOICES):
        self.field_choices = field_choices
        self.fields = {}
        for f in self.field_choices:
             self.fields.update({f:[]})
        self.comments = []

    def contact(self):
        return self.fields["contact"]

    def get_field(self, field):
        if not field in self.field_choices:
            return None
        return self.fields[field]

    def is_valid(self):
        return (len(self.contact()) != 0 and len(self.contact()[0]) != 0)

    def to_dict(self):
        r = {}
        for f in self.field_choices:
            if len(self.fields[f]) != 0:
                r.update({f : self.fields[f]})
        if len(self.comments) != 0:
            r.update({"comments" : self.comments})
        return r

    def parse(self, raw):
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        raw = raw.replace("<br>","")

        lines = raw.split("\n")
        for line in lines:
            line = line.strip()

            # Ignore empty and useless lines
            if not line or ":" not in line:
                continue

            # Comment
            if line.startswith("#"):
                self.comments.append(line.replace("#", "").strip())
                continue

            field, value = line.split(":", 1)
            value = value.strip()

            if field.lower() in self.field_choices and len(value) != 0:
                self.fields[field.lower()].append(value)

        return self.is_valid()

    def parse_url(self, url):
        url_parsed = urlparse(url)
        url = "{}://{}/.well-known/security.txt".format(
            url_parsed.scheme, url_parsed.netloc
        )

        try:
            resp = requests.get(url)
        except requests.exceptions.TooManyRedirects:
            return False
        except requests.exceptions.SSLError:
            return False

        if not resp.ok:
            return False

        self.parse(resp.content)

        return self.is_valid()
