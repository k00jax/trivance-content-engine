# Test script for posts.py endpoints using PowerShell
# Run this after starting the FastAPI server with: python -m uvicorn app.main:app --reload

Write-Host "🧩 Testing posts.py endpoints with PowerShell" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Test 1: Debug endpoint
Write-Host "`n1. Testing debug endpoint..." -ForegroundColor Yellow
$debugPayload = @{
    title = "Test Article"
    summary = "This is a test summary for debugging purposes"
    source = "Test Source"
    url = "https://example.com"
    style = "consultative"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/posts/debug" -Method Post -Body $debugPayload -ContentType "application/json"
    Write-Host "✅ Debug Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Debug failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Generate endpoint (correct format)
Write-Host "`n2. Testing generate endpoint (correct format)..." -ForegroundColor Yellow
$generatePayload = @{
    title = "AI Revolution in Small Business"
    summary = "This comprehensive article explores how artificial intelligence is transforming small business operations, offering new opportunities for automation, customer service, and strategic decision-making."
    source = "MIT Technology Review"
    link = "https://example.com/article"
    post_style = "consultative"
    platform = "LinkedIn"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/posts/generate" -Method Post -Body $generatePayload -ContentType "application/json"
    Write-Host "✅ Generate Response (correct format):" -ForegroundColor Green
    if ($response.post) {
        Write-Host "Post preview: $($response.post.Substring(0, [Math]::Min(100, $response.post.Length)))..." -ForegroundColor White
    }
    Write-Host "Response keys: $($response.PSObject.Properties.Name -join ', ')" -ForegroundColor Gray
} catch {
    Write-Host "❌ Generate failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "422 Validation Error - check field names and types" -ForegroundColor Red
    }
}

# Test 3: Generate endpoint (legacy format)
Write-Host "`n3. Testing generate endpoint (legacy format)..." -ForegroundColor Yellow
$legacyPayload = @{
    title = "Legacy Format Test"
    summary = "Testing backward compatibility with the old payload format that used url and style field names."
    url = "https://example.com/legacy-test"
    style = "punchy"
    platform = "LinkedIn"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/posts/generate" -Method Post -Body $legacyPayload -ContentType "application/json"
    Write-Host "✅ Generate Response (legacy format):" -ForegroundColor Green
    if ($response.post) {
        Write-Host "Post preview: $($response.post.Substring(0, [Math]::Min(100, $response.post.Length)))..." -ForegroundColor White
    }
} catch {
    Write-Host "❌ Legacy generate failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Hashtag endpoint
Write-Host "`n4. Testing hashtag endpoint..." -ForegroundColor Yellow
$hashtagPayload = @{
    content = "Artificial intelligence is revolutionizing small business operations through automation and strategic insights for entrepreneurs."
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/posts/hashtags" -Method Post -Body $hashtagPayload -ContentType "application/json"
    Write-Host "✅ Hashtag Response:" -ForegroundColor Green
    Write-Host "Generated hashtags: $($response.hashtags -join ', ')" -ForegroundColor White
} catch {
    Write-Host "❌ Hashtag failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎯 Test Summary" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host "✅ All tests completed!" -ForegroundColor Green
Write-Host "Expected results:" -ForegroundColor White
Write-Host "- Debug endpoint: 200 with received keys and payload" -ForegroundColor Gray
Write-Host "- Generate endpoints: 200 with post content" -ForegroundColor Gray
Write-Host "- Hashtag endpoint: 200 with hashtag array" -ForegroundColor Gray
Write-Host "- If you see 422 errors, check field names and validation" -ForegroundColor Gray
