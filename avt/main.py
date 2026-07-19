import sys
from pypdf import PdfReader

def usage() -> None:
    print("Usage:", sys.argv[0], " <in.pdf>")

def main() -> None:
    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

    # Load your locked or digitally signed PDF
    reader = PdfReader(sys.argv[1])

    # Retrieve the raw interactive form field data dictionary
    fields = reader.get_fields()

    if fields:
        print(f"{'FIELD NAME':<35} | {'VALUE'}")
        print("-" * 60)
        for field_name, field_attributes in fields.items():
            # Extracted value from the /V key of the PDF object
            value = field_attributes.get("/V", "")

            # Filter out empty signatures or layout artifacts
            if value:
                print(f"{field_name:<35} | {value}")
    else:
        print("No interactive form data fields found in the document structure.")
