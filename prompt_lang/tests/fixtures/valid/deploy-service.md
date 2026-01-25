---
name: deploy-service
description: Deploys a service to production after validation. Use when deploying new releases.
tools: Bash, Read
---

# Deploy Service

<purpose>
Automate production deployment with pre-flight validation checks.
</purpose>

<variables>
| Variable | Description | Default |
|----------|-------------|---------|
| `$1` | Service name | Required |
| `$2` | Environment | production |
</variables>

<context>
This skill is used in CI/CD pipelines. It assumes the service has already been built and tested.
</context>

<instructions>
1. VERIFY the service exists
   ```bash
   python scripts/check_service.py $1
   ```
2. EXECUTE pre-flight checks
   ```bash
   python scripts/preflight.py $1 $2
   ```
3. EXECUTE deployment to environment
   ```bash
   bash scripts/deploy.sh $1 $2
   ```
4. VERIFY deployment health
   ```bash
   python scripts/healthcheck.py $1 $2
   ```
</instructions>

<workflow>
START → Validate → Pre-flight → Deploy → Health check → END
</workflow>

<constraints>
- Do not deploy without passing pre-flight checks
- Do not skip health check verification
- Do not modify deployment scripts during execution
</constraints>

<output>
- **Service**: $1
- **Environment**: $2
- **Status**: [Deployed | Failed]
- **Health**: [Healthy | Unhealthy]
</output>

<criteria>
- [ ] Service validated
- [ ] Pre-flight passed
- [ ] Deployment completed
- [ ] Health check passed
</criteria>
