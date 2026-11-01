# genpark-agentic-commerce-supply-chain-bullwhip-order-variance-dampener-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Multi-echelon supply chain Bullwhip Effect amplifier dampener, demand distortion index & smoothing filter.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `dampen_supply_chain_bullwhip`
- **Category**: `agentic_commerce`

### Method Documentation
Quantify and dampen the Bullwhip Effect demand variance amplification across multi-echelon supply chains.
Bullwhip Measure = (Variance of Orders / Mean of Orders) / (Variance of Demand / Mean of Demand).
Calculates upstream distortion amplification ratio and provides Holt-Winters exponential smoothing allocation.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "dampen_supply_chain_bullwhip",
    "arguments": {
    "consumer_demands": [
        100,
        110,
        95,
        105,
        115,
        98
    ],
    "upstream_orders": [
        80,
        140,
        70,
        150,
        160,
        65
    ],
    "smoothing_alpha": 0.3
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
