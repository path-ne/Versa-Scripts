# Versa-Scripts

A collection of Python scripts for automating Versa SD-WAN device upgrade validation and management.

## Overview

This repository contains automation scripts designed to validate and manage Versa SD-WAN appliance upgrades. The primary script, `Versa_Upgrade_Validation.py`, orchestrates a complete upgrade workflow with health checks, template synchronization, and post-upgrade validation.

## Repository Structure

### Main Script
- **`Versa_Upgrade_Validation.py`** - The main upgrade validation script that handles the complete upgrade lifecycle for Versa SD-WAN devices

### Dependencies
- **`Dependencies.py`** - Provides utility functions and API helper methods used by the main script

### Additional
- **`side_by_side.py`** - Helper module for side-by-side output formatting (imported by main script)

## Key Features

### Dependencies Module (`Dependencies.py`)

Provides critical configuration and API helper functions:

#### Configuration Variables
- `dep_versa_user` - Service account username for Versa Director API
- `dep_versa_pass` - Service account password
- `dep_base_url` - Base URL for Versa Director (e.g., `https://sdwan.test.cloud:9182/`)
- `headers` - HTTP headers for API requests (JSON content type)

#### API Helper Functions

1. **`template_sync_status(device)`** - Checks template synchronization status with the Versa Director
2. **`get_osspack(device)`** - Retrieves current OSSPack version for a device
3. **`install_osspack(device, os)`** - Installs a specified OSSPack version (trusty or bionic)
4. **`get_workflow_device(device)`** - Fetches device workflow configuration and metadata
5. **`redeploy_device_workflow(device)`** - Redeploys the device workflow template
6. **`commit_template(device)`** - Commits configuration templates to the device
7. **`get_version(device)`** - Retrieves device package information and version details

### Main Script (`Versa_Upgrade_Validation.py`)

Orchestrates a 10-step upgrade validation process:

#### Pre-Upgrade Phase
1. **Health Verification** - Captures device health metrics (interfaces, BGP, IKE, SD-WAN datapaths)
2. **Alert Collection** - Gathers any active alerts
3. **Template Sync Validation** - Ensures device templates are synchronized with the Director
4. **OSSPack Verification** - Checks and installs Trusty OSSPack v20230629 if needed

#### Upgrade Phase
5. **Service Template Configuration** - Adds bionic upgrade service template to device
6. **Manual Upgrade** - Prompts user to perform manual upgrade via Versa Orchestrator

#### Post-Upgrade Phase
7. **Health Revalidation** - Monitors device health and waits for successful upgrade completion
8. **Template Sync Verification** - Confirms post-upgrade template synchronization
9. **OSSPack Installation** - Installs Bionic OSSPack v20230629
10. **Cleanup & Notification** - Removes bionic service template and sends Teams notification with health comparison

## Usage

### Prerequisites
- Python 3.x
- `requests` library for HTTP API calls
- Access to Versa Director REST API
- Valid service account credentials configured in `Dependencies.py`
- Microsoft Teams webhook URL for notifications (configured in main script)

### Running the Script

```bash
python Versa_Upgrade_Validation.py
```

When prompted, enter the target device name:
```
Enter device name:
your-device-name
```

The script will guide you through each step, prompting for user action where required (e.g., initiating the manual upgrade in Versa Orchestrator).

## Configuration

Before running the script, update the following in `Dependencies.py`:
- `dep_versa_user` - Your service account username
- `dep_versa_pass` - Your service account password
- `dep_base_url` - Your Versa Director API endpoint

In `Versa_Upgrade_Validation.py`, configure:
- `webhook` - Your Microsoft Teams webhook URL for success notifications

## Monitoring & Output

The script provides detailed console output including:
- Device health status before and after upgrade
- Active alerts and changes
- Package/version information
- Template synchronization status
- OSSPack installation progress
- Side-by-side comparison of pre/post-upgrade metrics
- Teams webhook notification with health dashboard (on success)

## Backoff Configuration

Default retry parameters in main script:
- `backoffs["wait"]` - 60 seconds between health checks
- `backoffs["success_wait"]` - 390 seconds after upgrade completion
- `backoffs["max_tries"]` - 180 retry attempts (3 hours total)
- `osspack["wait"]` - 60 seconds between OSSPack status checks
- `osspack["max_tries"]` - 20 retry attempts

## Error Handling

The script includes robust error handling:
- Graceful handling of API failures with retry logic
- OSSPack installation timeout detection
- Template synchronization validation with user intervention prompts
- Device reachability checks during upgrade monitoring

## License

MIT License - See LICENSE file for details

## Support

For issues or questions about these scripts, please open an issue in the repository.

---

**Note:** This repository is designed for automation of Versa SD-WAN device upgrades. Ensure proper testing in a non-production environment before deploying to production devices.
