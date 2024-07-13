import requests
import hashlib
import os
import subprocess

# Step 1: Get the Expected Hash Value of the VLC Installer
hash_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
response = requests.get(hash_url)
if response.status_code == 200:
    hash_text = response.text
    expected_hash = hash_text.split()[0]
else:
    raise Exception("Failed to download hash file.")

# Step 2: Download the VLC Installer
installer_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
installer_response = requests.get(installer_url)
if installer_response.status_code == 200:
    installer_content = installer_response.content
else:
    raise Exception("Failed to download VLC installer.")

# Step 3: Verify the Integrity of the Downloaded VLC Installer
computed_hash = hashlib.sha256(installer_content).hexdigest()
if computed_hash != expected_hash:
    raise Exception("Hash values do not match. Aborting installation.")

# Step 4: Save the Downloaded VLC Installer to Disk
temp_path = os.path.join(os.getenv('TEMP'), 'vlc-3.0.17.4-win64.exe')
with open(temp_path, 'wb') as file:
    file.write(installer_content)

# Step 5: Silently Run the VLC Installer
subprocess.run([temp_path, '/L=1033', '/S'])

# Step 6: Delete the VLC Installer from Disk
os.remove(temp_path)
