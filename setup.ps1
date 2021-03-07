$path = $(get-location)
$administrator = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())

if ($administrator.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    if ([System.IO.File]::Exists("$($path)/clines.exe")) {
        echo "`nThis directory must be added to path in order to use the 'clines.exe' program."
        echo "`nTo edit or permanently remove the directory from path, use Windows registry or`nthe environment variables GUI (Settings -> System -> Advanced system`nsettings -> Environment Variables...)`n"
        echo "Directory: $($path)"
        $decision = Read-Host -Prompt "`nAre you sure you want to add this directory to path? [Y/n]"
        if ($decision -eq "y") {
            setx /M PATH "$Env:PATH;$($path)"
            echo "`nDirectory successfully added to path. You can now run the 'clines.exe' program`nby typing 'clines' in your terminal`n"
        } else {
            echo "Cancelling setup. 'clines.exe' will not be added to path`n"
        }
    } else {
        echo "`n'clines.exe' could not found in the current directory:`n'$($path)'"
        echo "`nPlease make sure that this script is located in the exact same`ndirectory as the 'clines.exe' program`n"
    }
} else {
    echo "`nPlease run this script as an Administartor`n"
}

pause