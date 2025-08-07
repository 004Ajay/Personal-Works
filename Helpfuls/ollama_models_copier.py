## Python Script to generate commands to copy ollama models to other computers in your network.

## Assumptions:
### 1. Ollama is installed on both systems (as installation will create required directories)

## Inputs: Path to manifest file, destination computer username, destination computer IP address

## Outputs: 3 commands (1 SSH & 2 SCP)
#               - SSH command for making required folders.
#               - 1st SCP command for copying the manifest file, and
#               - 2nd SCP command for copying the blobs

import os
import json

print("\n")

# manifest file path
manifest_path = input(f"""Please give path to the ollama manifest file(content inside it maybe in JSON format)\nSample path '/home/appuser/.ollama/models/manifests/registry.ollama.ai/library/qwen3/4b'\nEnter path here: """).strip()

print(f"\nOllama Manifest path given by you: '{manifest_path}'\n")

try:
    manifest_dir_path = os.path.dirname(manifest_path) # removes the ending 4b, 20b like filename from the path
    if "manifests" in manifest_path:
        blobs_path = manifest_path.split("manifests")[0] + "blobs"
except Exception as e:
    print(f"Error: {e}")
    exit(1)

print(f"""I created some paths automatically.
Current system's ollama blobs path: '{blobs_path}'
Destination Manifest path: '{manifest_path}'
Destination Blobs path: '{blobs_path}'\n""")

try:
    with open(manifest_path, 'r') as f:
        manifest = json.load(f) # load and parse manifest JSON
except FileNotFoundError:
    print(f"Error: Manifest file not found at path '{manifest_path}'")
    exit(1)
except json.JSONDecodeError:
    print("Error: Manifest file is not a valid JSON.")
    exit(1)
except Exception as e:
    print(f"Unexpected error reading manifest file: {e}")
    exit(1)

digests = [] # SHA256 digests

# include the config digest
try:
    if "config" in manifest and "digest" in manifest["config"]:
        digests.append(manifest["config"]["digest"])
except Exception as e:
    print(f"Error extracting config digest: {e}")
    exit(1)

# include all layer digests
try:
    for layer in manifest.get("layers", []):
        digests.append(layer.get("digest"))
except Exception as e:
    print(f"Error extracting layer digest: {e}")
    exit(1)

# making sha256 file names to match filename at blobs location
try:
    correct_digests = [digest.replace(':', '-') for digest in digests]
except Exception as e:
    print(f"Error processing digest filenames: {e}")
    exit(1)

# generating scp commands
source_user = input(f"""Enter your destination computer username (Sample: appuser)\nEnter username here: """).strip()

print()

source_ip = input(f"""Enter your destination computer IP Address (Sample: 192.168.1.230)\nEnter IP Address here: """).strip()

if not source_user or not source_ip: # if user skips entering the source name and ip
    print("Error: Username or IP address cannot be empty.")
    exit(1)

print("\n\n#### Run the following commands from this computer ####\n")

# SSH command - for making folders
print("\nSSH command for making folders:\n")
print(f"ssh {source_user}@{source_ip} 'mkdir -p {manifest_dir_path}'")

# Manifest SCP command
print("\n\nManifest file scp command:\n")
print(f"sudo scp {manifest_path} {source_user}@{source_ip}:{manifest_path}")

# Blob files SCP command
print("\n\nBlob files scp command:\n")

scp_command = "sudo scp"

# blob files paths
for filename in correct_digests:
    full_path = os.path.join(blobs_path, filename)
    scp_command += f" {full_path}"

# Final destination path (we assume the files should land in the same structure)
scp_command += f" {source_user}@{source_ip}:{blobs_path}"

print(scp_command)

print("\n\n## Info:\nThere are three commands, first one for making required folders, second for copying the manifest file and third for copying the blobs. Make sure you copy and enter both the commands.\nIf any auto-created path is wrong, correct in the final 'scp' commands.\nIt is better to make edits in the python code, for ex: addition of 'sudo' infront of all scp commands.\n\n")