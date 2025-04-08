# Run PyInstaller with the provided spec file
pyinstaller --clean --noconfirm pyinstaller_bootstrapper.spec

# Define paths
$distFolder = "dist"
$exeName = "NemoLibraryUI.exe"
$issFile = "installer_script.iss"
$outputInstaller = "Output\NemoLibrarySetup.exe"  # Updated path to match Inno Setup output

# Change to the dist folder
Set-Location $distFolder

# Return to the original directory
Set-Location ..

# Remove the destination file if it already exists
if (Test-Path "$distFolder\NemoLibrarySetup.exe") {
    Remove-Item -Path "$distFolder\NemoLibrarySetup.exe" -Force -ErrorAction SilentlyContinue
}

# Use Inno Setup to create a setup file
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" $issFile

# Move the generated installer to the dist folder
Move-Item -Path ".\$outputInstaller" -Destination "$distFolder\NemoLibrarySetup.exe"

# Remove the empty Output folder
Remove-Item -Path "Output" -Recurse -Force -ErrorAction SilentlyContinue

# Remove $exeName from the dist folder
Remove-Item -Path "$distFolder\$exeName" -Force -ErrorAction SilentlyContinue
