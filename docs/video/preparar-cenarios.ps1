<#
Prepara, pela API REAL e com dados fictícios do seed, os cenários de conflito, remarcação e cancelamento.
Não usa IDs fixos e não mexe direto no banco. Use preferencialmente com um banco descartável.
Uso:  powershell -ExecutionPolicy Bypass -File docs/video/preparar-cenarios.ps1 [-Api http://127.0.0.1:8000]
#>
param([string]$Api = "http://127.0.0.1:8000")
$ErrorActionPreference = "Stop"
$h = @{ "Content-Type" = "application/json" }

$clients = Invoke-RestMethod "$Api/api/clients"
$services = Invoke-RestMethod "$Api/api/services"
$appts = Invoke-RestMethod "$Api/api/appointments"
$now = Get-Date

# 1) Agendamento existente de Carla Demo (agendado, futuro) = base do CONFLITO
$carla = $appts | Where-Object { $_.client.name -eq "Carla Demo" -and $_.status -eq "SCHEDULED" -and [datetime]$_.start_at -gt $now } | Sort-Object start_at | Select-Object -First 1
if (-not $carla) { throw "Nao ha agendamento futuro de Carla Demo. Rode o seed em um banco novo (veja o HANDOFF)." }
$cStart = [datetime]$carla.start_at
$conflictTry = $cStart.AddMinutes(15)

# 2) Base de REMARCACAO/CANCELAMENTO: Elisa Modelo, Corte de cabelo, dia seguinte ao da Carla, 14:00
$elisa = $clients | Where-Object { $_.name -eq "Elisa Modelo" } | Select-Object -First 1
$corte = $services | Where-Object { $_.name -eq "Corte de cabelo" } | Select-Object -First 1
$baseStart = $cStart.Date.AddDays(1).AddHours(14)
$existing = $appts | Where-Object { $_.client.name -eq "Elisa Modelo" -and $_.status -eq "SCHEDULED" -and ([datetime]$_.start_at) -eq $baseStart } | Select-Object -First 1
if ($existing) {
    $base = $existing
    Write-Host "Base ja existe (id $($base.id))."
} else {
    $body = @{ client_id = $elisa.id; service_id = $corte.id; start_at = $baseStart.ToString("yyyy-MM-ddTHH:mm:ss") } | ConvertTo-Json
    $base = Invoke-RestMethod -Method Post -Uri "$Api/api/appointments" -Headers $h -Body $body
    Write-Host "Base criada (id $($base.id))."
}

Write-Host ""
Write-Host "CENARIOS PARA GRAVAR (use estas datas na interface):"
Write-Host ("1 Conflito    : cliente Bruno Teste, servico Barba, {0:dd/MM/yyyy HH:mm}  (Carla Demo ocupa {1:HH:mm}-{2:HH:mm})" -f $conflictTry, $cStart, ([datetime]$carla.end_at))
Write-Host ("2 Remarcacao  : Elisa Modelo de {0:dd/MM/yyyy HH:mm} para {1:dd/MM/yyyy HH:mm}" -f $baseStart, $baseStart.AddHours(1))
Write-Host "3 Cancelamento: o mesmo agendamento de Elisa Modelo, depois da remarcacao"
Write-Host ("(ids desta base de dados: Carla={0}, Elisa={1}; nao valem em outro banco)" -f $carla.id, $base.id)
