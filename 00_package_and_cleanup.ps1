# Run PyInstaller with the provided spec file
pyinstaller --noconfirm --onefile --console 01_bootstrapper.py --name NemoUI

# sign the executable
./ext/sign_executable.ps1

# # Define paths
# $distFolder = "dist"
# $exeName = "NemoUI.exe"
# $setupexe = "NemoUISetup.exe"
# $issFile = "installer_script.iss"
# $outputInstaller = "Output\$setupexe"  # Updated path to match Inno Setup output

# # Change to the dist folder
# Set-Location $distFolder

# # Return to the original directory
# Set-Location ..

# # Remove the destination file if it already exists
# if (Test-Path "$distFolder\$setupexe") {
#     Remove-Item -Path "$distFolder\$setupexe.exe" -Force -ErrorAction SilentlyContinue
# }

# # Use Inno Setup to create a setup file
# & "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" $issFile

# # Move the generated installer to the dist folder
# Move-Item -Path ".\$outputInstaller" -Destination "$distFolder\$setupexe.exe"

# # Remove the empty Output folder
# Remove-Item -Path "Output" -Recurse -Force -ErrorAction SilentlyContinue

# # Remove $exeName from the dist folder
# Remove-Item -Path "$distFolder\$exeName" -Force -ErrorAction SilentlyContinue
