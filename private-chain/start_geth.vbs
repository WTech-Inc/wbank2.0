Dim WshShell
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "E:\wbank\private-chain"
WshShell.Run "E:\wbank\private-chain\geth.exe --dev --http --http.addr 0.0.0.0 --http.port 8545 --http.api eth,web3,net,personal --http.corsdomain * --http.vhosts * --nodiscover --ipcdisable --dev.gaslimit 9999999999", 0, False
