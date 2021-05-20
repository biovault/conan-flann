Param(
    [Parameter(Mandatory=$true)]
    [String] $PackageName,
)

$REGEX_TESTING='^testing/(.*)_dual$'
$REGEX_STABLE='^stable/(.*)_dual$'
$REGEX_TAG='^(.*)_dual'
$branch=[Environment]::GetEnvironmentVariable('APPVEYOR_REPO_BRANCH')

if ( ([Environment]::GetEnvironmentVariable('APPVEYOR_REPO_TAG' -eq 'true') -and 
     ([Environment]::GetEnvironmentVariable('APPVEYOR_REPO_TAG_NAME') -match $REGEX_TAG) ) {
    $reference=$PackageName+'/'+$Matches.1+'@lkeb/stable'
    [System.Environment]::SetEnvironmentVariable('CONAN_REFERENCE',$reference, 'User')
}
elseif ($branch -match $REGEX_STABLE) {
    $reference=$PackageName+'/'+$Matches.1+'@lkeb/stable'
    [System.Environment]::SetEnvironmentVariable('CONAN_REFERENCE',$reference, 'User')
}
elseif ($branch -match $REGEX_TESTING) {
    $reference=$PackageName+'/'+$Matches.1+'@lkeb/testing'
    [System.Environment]::SetEnvironmentVariable('CONAN_REFERENCE',$reference, 'User')
}
else {
    Write-Output "Error in set_appveyor_conan_reference"
    Write-Output "Expected either:"
    Write-Output "1:  a APPVEYOR_REPO_TAG_NAME with a version number and '_dual' suffix"
    Write-Output "2:  a APPVEYOR_REPO_BRANCH with 'testing/.*_dual' or 'stable/.*_dual'"
}