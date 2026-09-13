import os
import glob
import re

BRACKETS_DIR = os.path.join("content", "brackets")

def convert_weight_to_extra():
    if not os.path.exists(BRACKETS_DIR):
        print(f"❌ Directory not found: {BRACKETS_DIR}")
        return

    updated_count = 0

    for filepath in glob.glob(os.path.join(BRACKETS_DIR, "*.md")):
        filename = os.path.basename(filepath)
        if filename == "_index.md":
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Match TOML front-matter bounded by +++
        pattern = r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            continue

        front_matter = match.group(1)
        body = match.group(2)

        # Check if root-level weight exists
        weight_match = re.search(r"^weight\s*=\s*(\d+)", front_matter, re.MULTILINE)

        if weight_match:
            extracted_weight = weight_match.group(1)

            # Remove root-level weight line
            front_matter = re.sub(r"^weight\s*=\s*\d+\s*\n?", "", front_matter, flags=re.MULTILINE)

            # Inject weight = X directly under the [extra] header
            if "[extra]" in front_matter:
                front_matter = front_matter.replace("[extra]", f"[extra]\nweight = {extracted_weight}")
            else:
                front_matter = front_matter.strip() + f"\n\n[extra]\nweight = {extracted_weight}\n"

            # Reconstruct clean markdown file content
            new_content = f"+++\n{front_matter.strip()}\n+++\n{body}"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

            updated_count += 1
            print(f"✓ Shifted weight to [extra] in: {filename}")

    print(f"\nSuccessfully updated {updated_count} match files!")

if __name__ == "__main__":
    convert_weight_to_extra()