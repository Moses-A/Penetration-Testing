#Written by Moses Arocha

$Entry_message = "Welcome To The Basic Ping Scan"
$answer = " Would You Like To Grab IP's From A File?"

$yes = New-Object System.Management.Automation.Host.ChoiceDescription "&Yes", `
    " Extracting IP's From A File If Chosen."

$no = New-Object System.Management.Automation.Host.ChoiceDescription "&No", `
    " Manually Enter In All IP's For Ping."

$options = [System.Management.Automation.Host.ChoiceDescription[]]($yes, $no)

$result = $host.ui.PromptForChoice($Entry_message, $answer, $options, 0) 

switch ($result)
    {
        0 {
           $names = Get-content "C:\Users\s591810\Desktop\computerlist.txt"
		foreach ($name in $names)
                {
                 if (Test-Connection -ComputerName $name -Count 1 -ErrorAction SilentlyContinue)
                 {
                  Write-Host "$name Ping Successful"
                 }
                 else
                 {
                 Write-Host "$name Ping Failure" -ForegroundColor Red
                 }
                }
         }
        1 {
           $IPs = Read-Host - Prompt " What IP Would You Like To Ping?"
		foreach ($IP in $IPs)
                {
                 if (Test-Connection -ComputerName $IP -Count 1 -ErrorAction SilentlyContinue)
                 {
                  Write-Host "$IP Ping Successful"
                 }
                 else
                 {
                  Write-Host "$IP Ping Failure" -ForegroundColor Red
                 }
                }
}
    }
