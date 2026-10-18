# DGM-Contracts — Shared Public Interfaces

This repository is a shared-contract package only. It may contain stable public data models, event schemas, service-port protocols, version definitions and contract tests used by DGM-MAT core and approved satellite packages.

It must not contain orchestration, runtime policy, provider implementations, persistence engines or UI. Check consumers before changing contracts. DGM-MAT-Agents is a known candidate consumer; validate actual imports before migration.