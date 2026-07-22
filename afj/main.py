import os
import sys
import json
from pypdf import PdfReader

def usage() -> None:
    print("Usage:", sys.argv[0], " <in.pdf>")

def strip_name(name) -> str:
    if name == None:
        return "UNCHECKED"
    if name.startswith("/"):
        return name[1:]
    return name

# PDF standard requies lines to be separated with '\r'.  Switch to the native newline.
def native_newline(s: str) -> str:
    lines = s.splitlines()
    return os.linesep.join(lines)

def main() -> None:
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    # Load your locked or digitally signed PDF
    reader = PdfReader(sys.argv[1])

    # Retrieve the raw interactive form field data dictionary
    fields = reader.get_fields()

    fdict = {}

    if fields:
        for field_name, field in fields.items():
            value = field.value

            if field.field_type == "/Tx":
                fdict[field_name] = native_newline(value)
            elif field.field_type == "/Btn":
                fdict[field_name] = strip_name(value)
            else: # for unknown field types, just output the type
                fdict[field_name] = field.field_type
    else:
        print("No interactive form data fields found in the document structure.")

    # Convert to a JSON string
    print(json.dumps(fdict))
