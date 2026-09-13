import os
import tomllib  # Built-in in Python 3.11+. Use `import toml` if on older Python versions.

# Define project paths
STATIONS_TOML_PATH = os.path.join("data", "stations.toml")
STATIONS_CONTENT_DIR = os.path.join("content", "stations")


def generate_station_markdown_files():
    # 1. Ensure the destination directory exists
    os.makedirs(STATIONS_CONTENT_DIR, exist_ok=True)

    # 2. Ensure section _index.md exists in content/stations/
    index_path = os.path.join(STATIONS_CONTENT_DIR, "_index.md")
    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(
                '+++\ntitle = "All Stations"\ntemplate = "stations_section.html"\n+++\n'
            )
        print(f"✓ Created section index: {index_path}")

    # 3. Read and parse data/stations.toml
    if not os.path.exists(STATIONS_TOML_PATH):
        print(f"❌ Error: Could not find '{STATIONS_TOML_PATH}'.")
        return

    with open(STATIONS_TOML_PATH, "rb") as f:
        stations_data = tomllib.load(f)

    # 4. Iterate over station entries and create markdown files
    created_count = 0
    for key, data in stations_data.items():
        # Skip top-level non-dictionary metadata (e.g. total_stations = 10)
        if not isinstance(data, dict):
            continue

        station_id = data.get("id", key)
        station_name = data.get("name", key)

        # File name matches the station ID (e.g., content/stations/the_barnyard.md)
        file_path = os.path.join(STATIONS_CONTENT_DIR, f"{station_id}.md")

        front_matter = f"""+++
title = "{station_name}"
template = "station_page.html"

[extra]
station_id = "{station_id}"
+++
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(front_matter)

        print(f"  ➜ Generated: {file_path} (ID: {station_id})")
        created_count += 1

    print(
        f"\n✓ Successfully generated {created_count} station markdown files in '{STATIONS_CONTENT_DIR}/'!"
    )


if __name__ == "__main__":
    generate_station_markdown_files()