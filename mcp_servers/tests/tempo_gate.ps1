#!/usr/bin/env pwsh
# TEMPO Quality Gate — consolidated gate script [D-1]
# Usage: .\tempo_gate.ps1
# Exit 0 = all checks pass. Exit 1 = one or more checks failed.

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$pass = $true

function Test-Gate {
    param([string]$Name, [scriptblock]$Block)
    Write-Host "  [$Name]" -NoNewline
    try {
        & $Block
        Write-Host " PASS" -ForegroundColor Green
    } catch {
        Write-Host " FAIL: $_" -ForegroundColor Red
        $script:pass = $false
    }
}

Write-Host "`nTEMPO Quality Gate" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

# 1. Standard tests (not benchmark)
Test-Gate "standard-tests" {
    & "$root\.venv\Scripts\python.exe" -m pytest "$root\mcp_servers\tests" -m "not benchmark" -q --tb=short
    if ($LASTEXITCODE -ne 0) { throw "pytest standard tests failed" }
}

# 2. Benchmark tests
Test-Gate "benchmark-tests" {
    & "$root\.venv\Scripts\python.exe" -m pytest "$root\mcp_servers\tests" -m "benchmark" -q --tb=short
    if ($LASTEXITCODE -ne 0) { throw "pytest benchmark tests failed" }
}

# 3. py_compile all workflow + benchmark modules
Test-Gate "py-compile" {
    $files = Get-ChildItem "$root\mcp_servers\workflow","$root\mcp_servers\benchmark" -Recurse -Filter "*.py" |
             Where-Object { $_.FullName -notlike "*__pycache__*" }
    foreach ($f in $files) {
        & "$root\.venv\Scripts\python.exe" -m py_compile $f.FullName
        if ($LASTEXITCODE -ne 0) { throw "py_compile failed: $($f.FullName)" }
    }
}

# 4. Lint
Test-Gate "ruff-lint" {
    & "$root\.venv\Scripts\python.exe" -m ruff check "$root\mcp_servers" --exclude .install
    if ($LASTEXITCODE -ne 0) { throw "ruff returned errors" }
}

# 5. Security scan
Test-Gate "bandit-security" {
    & "$root\.venv\Scripts\python.exe" -m bandit -r "$root\mcp_servers" -ll -q
    if ($LASTEXITCODE -ne 0) { throw "bandit found medium+ issues" }
}

# 6. ATLAS residue in code
Test-Gate "no-atlas-in-code" {
    $hits = Get-ChildItem "$root\mcp_servers" -Recurse -Filter "*.py" -File |
            Where-Object { $_.FullName -notlike "*__pycache__*" -and $_.FullName -notlike "*.install*" -and $_.Name -ne "test_integration_namespace.py" } |
            Select-String -Pattern "atlas\." -ErrorAction SilentlyContinue | 
            Select-Object -First 3
    if ($hits) { throw "atlas. residue found" }
}

# 7. AtlasConfig residue
Test-Gate "no-atlasconfig" {
    $hits = Get-ChildItem "$root\mcp_servers" -Recurse -Filter "*.py" -File |
            Where-Object { $_.FullName -notlike "*__pycache__*" -and $_.FullName -notlike "*.install*" -and $_.Name -ne "test_integration_namespace.py" } |
            Select-String -Pattern "AtlasConfig" -ErrorAction SilentlyContinue
    if ($hits) { throw "AtlasConfig residue found" }
}

# 8. ATLAS residue in docs
Test-Gate "no-atlas-in-docs" {
    $targets = @(
        "$root\.github\copilot-instructions.md",
        "$root\.github\prompts\assess-implement-gate.md",
        "$root\.github\prompts\systems-diagram-brief.md",
        "$root\.github\prompts\adr-template.md"
    )
    foreach ($t in $targets) {
        if (Test-Path $t) {
            $hits = Select-String -Path $t -Pattern "atlas" -CaseSensitive:$false
            if ($hits) { throw "atlas residue in $t" }
        }
    }
    $agentHits = Select-String -Path "$root\.github\agents\*.agent.md" -Pattern "atlas\." -ErrorAction SilentlyContinue
    if ($agentHits) { throw "atlas. residue in agent files" }
}

# 9. ATLAS residue in memory
Test-Gate "no-atlas-in-memory" {
    $hits = Select-String -Path "$root\.github\memory.md" -Pattern "^# ATLAS" -ErrorAction SilentlyContinue
    if ($hits) { throw "memory.md header still says ATLAS" }
}

# 10. Agent file renames verified
Test-Gate "agent-file-renames" {
    $stale = @("atlas-planner.agent.md","atlas-synthesizer.agent.md","atlas-reviewer.agent.md")
    foreach ($s in $stale) {
        if (Test-Path "$root\.github\agents\$s") { throw "Stale agent file still exists: $s" }
    }
    $expected = @("tempo-planner.agent.md","tempo-synthesizer.agent.md","tempo-reviewer.agent.md")
    foreach ($e in $expected) {
        if (-not (Test-Path "$root\.github\agents\$e")) { throw "Missing agent file: $e" }
    }
}

Write-Host ""
if ($pass) {
    Write-Host "All gates passed." -ForegroundColor Green
    exit 0
} else {
    Write-Host "One or more gates FAILED." -ForegroundColor Red
    exit 1
}
