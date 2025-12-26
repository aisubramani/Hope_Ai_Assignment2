import pkg_resources
import sys

def extract_version():
    # Input file containing library names (no versions)
    input_file = "libraries.txt"

    # Output file with library==version
    output_file = "requirements.txt"

    # Get current Python version
    python_version = (
        f"{sys.version_info.major}."
        f"{sys.version_info.minor}."
        f"{sys.version_info.micro}"
    )

    # Read library names
    with open(input_file, "r") as file:
        libraries = [line.strip() for line in file if line.strip()]

    # Write Python version + library versions
    with open(output_file, "w") as output:
        # Python version (documentation & validation)
        output.write(f"python=={python_version}\n")

        for lib in libraries:
            try:
                version = pkg_resources.get_distribution(lib).version
                output.write(f"{lib}=={version}\n")
            except pkg_resources.DistributionNotFound:
                output.write(f"{lib}==<NOT INSTALLED>\n")
                print(f'Library "{lib}" is not installed.')

    print(f"✔ requirements1.txt created successfully: {output_file}")


if __name__ == "__main__":
    extract_version()