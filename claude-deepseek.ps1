$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="sk-fd1cafee355b40d7bacf521131267f1f"

$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"

Write-Host "BASE_URL =" $env:ANTHROPIC_BASE_URL
Write-Host "MODEL    =" $env:ANTHROPIC_MODEL
Write-Host "TOKEN?   =" $($env:ANTHROPIC_AUTH_TOKEN.Substring(0,8) + "...")

claude