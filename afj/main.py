import os
import sys
import json
import getopt

from pypdf import PdfReader, PdfWriter

def usage() -> None:
    print("Usage:", sys.argv[0], " [-l <data.json>] <in.pdf>")
    sys.exit(1)

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

def normalize_field_values(values):
    """Recursively replace '\n' with '\r' in all string values.
    Handles dicts, lists, and scalar strings.
    """
    if isinstance(values, dict):
        return {k: normalize_field_values(v) for k, v in values.items()}
    if isinstance(values, list):
        return [normalize_field_values(v) for v in values]
    if isinstance(values, str):
        return values.replace('\n', '\r')
    return values

def load_fields(json_path, pdf_path):
    """Load field values from a JSON file and write them into the PDF.

    The JSON file should map form field names to their desired values. The
    function reads the input PDF (the first positional argument on the command
    line), updates each page's form fields, and overwrites the original PDF with
    the new contents.
    """
    # Load field values from JSON and normalize newlines
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw_values = json.load(f)
        field_values = normalize_field_values(raw_values)
    except Exception as e:
        print(f"Error loading JSON file '{json_path}': {e}")
        sys.exit(1)

    # Open the input PDF (positional argument) – same logic as print_fields
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"Error reading PDF '{pdf_path}': {e}")
        sys.exit(1)

    # Create a writer based on the existing document
    writer = PdfWriter(clone_from=reader)

    # Update form fields on each page with the provided values
    for page in writer.pages:
        writer.update_page_form_field_values(page, field_values, auto_regenerate=False)

    # Ensure appearance streams are generated for viewers that need them
    # try:
        # writer.set_need_appearances_writer(True)
    # except Exception:
        # pass

    # Overwrite the original PDF with updated content
    try:
        with open(pdf_path, "wb") as out_f:
            writer.write(out_f)
    except Exception as e:
        print(f"Error writing PDF '{pdf_path}': {e}")
        sys.exit(1)


def print_fields(pdf_path):
    # Load the PDF file
    reader = PdfReader(pdf_path)

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

def main() -> None:

    json_path = None
    pdf_path = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:", ["json="])

        # Process the option list
        for opt, val in opts:
            if opt == "-l":
                json_path = val

        # After options, exactly one positional argument must remain: <file>
        if len(args) != 1:
            print("Error: a single <file> argument is required.")
            usage()

        pdf_path = args[0]

        if json_path != None:
            load_fields(json_path, pdf_path)
        else:
            print_fields(pdf_path)


    except getopt.GetoptError as err:
        print(err)
        usage()
