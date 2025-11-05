# API Rate Limiting 測試腳本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "API Rate Limiting 測試" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$apiUrl = "http://localhost:5001/api/auth/login"
$testData = @{
    email = "test@example.com"
    password = "wrongpassword"
} | ConvertTo-Json

Write-Host "測試登入端點 Rate Limiting (限制: 5 次/分鐘)" -ForegroundColor Yellow
Write-Host "URL: $apiUrl`n" -ForegroundColor Gray

for ($i = 1; $i -le 7; $i++) {
    try {
        $response = Invoke-WebRequest -Uri $apiUrl `
            -Method POST `
            -Body $testData `
            -ContentType "application/json" `
            -UseBasicParsing `
            -ErrorAction SilentlyContinue
        
        Write-Host "[$i] 狀態碼: $($response.StatusCode) - " -NoNewline
        Write-Host "✅ 請求成功" -ForegroundColor Green
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 429) {
            Write-Host "[$i] 狀態碼: 429 - " -NoNewline
            Write-Host "⛔ Rate Limit 觸發！" -ForegroundColor Red
            
            # 嘗試讀取錯誤訊息
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errorBody = $reader.ReadToEnd()
            Write-Host "    回應: $errorBody" -ForegroundColor DarkRed
        }
        else {
            Write-Host "[$i] 狀態碼: $statusCode - " -NoNewline
            Write-Host "⚠️  其他錯誤" -ForegroundColor Yellow
        }
    }
    
    Start-Sleep -Milliseconds 500
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "測試完成！" -ForegroundColor Green
Write-Host "預期結果：前 5 次請求成功，第 6-7 次被 Rate Limit 阻擋" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan