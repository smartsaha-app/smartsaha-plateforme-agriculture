
$docxPath = "C:\Users\ASUS\Desktop\Smartsaha-Doc\SmartSaha_MultiPlateforme.docx"
$tempZipPath = "$env:TEMP\SmartSaha.zip"
$tempExtractPath = "$env:TEMP\SmartSahaDoc"

if (Test-Path $tempExtractPath) { Remove-Item $tempExtractPath -Recurse -Force }
New-Item -ItemType Directory -Path $tempExtractPath -Force | Out-Null

Copy-Item $docxPath $tempZipPath -Force
Expand-Archive -Path $tempZipPath -DestinationPath $tempExtractPath -Force

$xmlPath = Join-Path $tempExtractPath "word\document.xml"
if (Test-Path $xmlPath) {
    [xml]$doc = Get-Content $xmlPath
    $ns = New-Object System.Xml.XmlNamespaceManager($doc.NameTable)
    $ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
    $texts = $doc.SelectNodes("//w:t", $ns)
    $allText = ($texts | ForEach-Object { $_.InnerText }) -join " "
    Write-Output $allText
} else {
    Write-Error "Could not find word/document.xml in the docx file."
}

Remove-Item $tempZipPath -Force
Remove-Item $tempExtractPath -Recurse -Force
