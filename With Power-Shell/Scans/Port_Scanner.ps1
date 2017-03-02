# Author is Moses Arocha

$Computer_IP = Read-Host -Prompt ' What Is The IP Address?'
$port_number = Read-Host -Prompt ' What Is The Port Number?'

echo "$Computer_IP, $port_number"

foreach ($i in {port_number}) {
try 
{
   $socket = new-object System.Net.Sockets.TCPClient(Computer_IP, $i);
    } catch {}

   if ($socket -eq $NULL) 
   {
      echo "$Computer_IP:$i - Closed";
   } 

   else 
   { 
      echo "$Computer_IP:$i - Open";
      $socket = $NULL;
   }
}
