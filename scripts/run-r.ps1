#Requires -Version 7.0
<#
Run project R code in a clean child process. No user or Windows settings change.
Example: .\scripts\run-r.ps1 -RArguments @('validation/smoke-check.R')
Override the two tool paths explicitly when moving this project to another PC.
#>
[CmdletBinding(PositionalBinding = $false)]
param(
    [string] $RscriptPath = 'D:\Softwares\Applications\R\R-4.5.0\bin\Rscript.exe',
    [string] $PandocDirectory = 'D:\Softwares\Applications\RStudio\resources\app\bin\quarto\bin\tools',
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [AllowEmptyString()]
    [string[]] $RArguments = @('--version')
)

$ErrorActionPreference = 'Stop'

try {
    if (-not (Test-Path -LiteralPath $RscriptPath -PathType Leaf)) {
        throw "Rscript executable not found: $RscriptPath. Supply -RscriptPath explicitly."
    }
    if (-not (Test-Path -LiteralPath (Join-Path $PandocDirectory 'pandoc.exe') -PathType Leaf)) {
        throw "Pandoc executable not found: $PandocDirectory. Supply -PandocDirectory explicitly."
    }

    $projectRoot = Split-Path -Parent $PSScriptRoot
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = (Resolve-Path -LiteralPath $RscriptPath).Path
    $startInfo.WorkingDirectory = $projectRoot
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    # Rscript accepts informational flags only before interpreter options.
    # These flags exit without starting an R session or running a script.
    if ($RArguments.Count -eq 0 -or $RArguments[0] -notin @('--version', '--help')) {
        $startInfo.ArgumentList.Add('--vanilla')
    }
    foreach ($argument in $RArguments) {
        # ArgumentList preserves spaces, quotes, and shell metacharacters.
        $startInfo.ArgumentList.Add($argument)
    }

    foreach ($name in @($startInfo.Environment.Keys)) {
        if ($name -eq 'LANG' -or $name -eq 'LANGUAGE' -or $name -like 'LC_*') {
            $startInfo.Environment.Remove($name) | Out-Null
        }
    }
    $startInfo.Environment['RSTUDIO_PANDOC'] = (Resolve-Path -LiteralPath $PandocDirectory).Path

    $child = [System.Diagnostics.Process]::new()
    $child.StartInfo = $startInfo
    try {
        $child.Start() | Out-Null
        # Read both pipes asynchronously to avoid one full pipe blocking R.
        $stdout = $child.StandardOutput.ReadToEndAsync()
        $stderr = $child.StandardError.ReadToEndAsync()
        $child.WaitForExit()
        $rExitCode = $child.ExitCode
        [Console]::Out.Write($stdout.GetAwaiter().GetResult())
        [Console]::Error.Write($stderr.GetAwaiter().GetResult())
    }
    finally {
        $child.Dispose()
    }
    exit $rExitCode
}
catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}
