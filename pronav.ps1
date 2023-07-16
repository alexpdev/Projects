# pronav.ps1

param (
    [int32]$P = 0,
    [switch]$Init = $false,
    [switch]$List = $false,
    [switch]$Update = $false,
    [string]$Root = $home,
    [string]$ProjectRoot = $home,
    [string]$Top = "$home\Documents",
    [int32]$Depth = 5
)

$PARENT = "$Root\.pronav"
$BASE = "$PARENT\.projects"

function Update-Root {
    Clear-Content -Path $BASE
    $exclusions = "*/AppData/*", "*/.git/*", "*/.tox/*", "*/__pycache__/*", "*/venv/*", "*/.cache/*"
    Get-ChildItem -Force -Directory -Path $TOP -Exclude $exclusions  -Include ".git" -Depth $Depth -ErrorAction SilentlyContinue |
    Foreach-Object {
        add-content $BASE $_.FullName
    }
    Get-Projects
}

function Start-Root {
    if (Test-Path $PARENT) {
        if (Test-Path $BASE){
            Update-Root
        } else {
            New-Item $BASE -ItemType File
            Update-Root
        }
    } else {
        New-Item -Path $PARENT -ItemType Directory
        New-Item -Path $BASE -ItemType File
        Update-Root
    }
}

function Get-Projects {
    $counter = 0
    $arr = Get-Content $Base
    $maxchars = 0
    foreach ($line in $arr){
        $projname = ((Split-Path $line -Parent) -split '\\')[-1]
        if ($projname.Length -gt $maxchars){
            $maxchars = $projname.Length
        }
    }
    Do
    {
        $line1 = $arr[$counter]
        $projdir1 = Split-Path $line1 -Parent
        $projname1 = ($projdir1 -split '\\')[-1]
        $out1 = "$counter : $projname1"
        $distance = $maxchars + 9 - $out1.Length

        if ($arr.Length -gt $counter+1){
            $counter2 = $counter + 1
            $line2 = $arr[$counter2]
            $projdir2 = Split-Path $line2 -Parent
            $projname2 = ($projdir2 -split '\\')[-1]
            $out2 = "$counter2 : $projname2"
            $mid = $(" " * $distance)
            write-host "$out1  $mid  $out2" -ForegroundColor DarkRed
        }
        else {write-host $out -ForegroundColor DarkRed}
        $counter = $counter + 2
    } until ($counter -ge $arr.length)
}


function Set-Project {
    $arr = Get-Content $BASE
    Set-Location (split-path $arr[$P] -parent)
}


If ($Init){
    Start-Root
} ElseIf ($List){
    Get-Projects
} ElseIf ($Update){
    Update-Root
} ElseIf ($P){
    Set-Project
}
