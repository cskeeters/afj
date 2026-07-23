`afj` is a CLI tool used to extract values from fields in PDF forms (AcroForm).

# Example

```sh
afj employee.pdf | jq
```

```json
{
  "first": "Chad",
  "last": "Skeeters",
  "citizen": "Off",
  "employment_type": "full-time",
  "hobbies": "Pickleball"
}
```

Extract individual values in a Bash.

```sh
FIRST=$(afj employee.pdf | jq -r '.first')
echo "Welcome to the team, $FIRST!"
```

Save current values to a JSON file.

```sh
afj employee.pdf > me.json
```

Load current values from a JSON file.

```sh
afj -l me.json employee.pdf
```

# Installation

```sh
brew install python uv
```

```sh
git clone git@github.com:cskeeters/afj.git
cd tyaf
# Requries uv to install the tool
make
```

# Related Tools

* [tyaf](https://github.com/cskeeters/tyaf)
* [aft](https://github.com/cskeeters/aft)
