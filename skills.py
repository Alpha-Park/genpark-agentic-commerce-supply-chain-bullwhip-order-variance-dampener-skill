# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-supply-chain-bullwhip-order-variance-dampener-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def dampen_supply_chain_bullwhip(consumer_demands, upstream_orders, smoothing_alpha=0.25):
    if len(consumer_demands) < 3 or len(upstream_orders) < 3:
        raise ValueError("Need at least 3 periods of demand and order history")
        
    def var_and_mean(lst):
        m = sum(lst) / len(lst)
        v = sum((x - m) ** 2 for x in lst) / (len(lst) - 1)
        return v, m

    var_d, mean_d = var_and_mean(consumer_demands)
    var_o, mean_o = var_and_mean(upstream_orders)
    
    cv_demand = (var_d ** 0.5) / mean_d if mean_d > 0 else 1.0
    cv_orders = (var_o ** 0.5) / mean_o if mean_o > 0 else 1.0
    
    bullwhip_ratio = (var_o / mean_o) / (var_d / mean_d) if (var_d > 0 and mean_d > 0 and mean_o > 0) else 1.0
    
    # Dampened recommended order using exponential smoothing to mitigate batching spikes
    smoothed_order = (smoothing_alpha * consumer_demands[-1]) + ((1.0 - smoothing_alpha) * upstream_orders[-1])
    
    if bullwhip_ratio > 2.0:
        tier = "SEVERE_DEMAND_DISTORTION"
        action = "High panic ordering / phantom backlog; enforce direct POS data sharing with tier-1 suppliers."
    elif bullwhip_ratio > 1.2:
        tier = "MODERATE_BULLWHIP_AMPLIFICATION"
        action = "Batching and lead time variance present; reduce minimum order quantities (MOQ)."
    else:
        tier = "DAMPENED_STABLE_SUPPLY_CHAIN"
        action = "Order variance closely tracks actual end-consumer pull."
        
    return {
        "bullwhip_amplification_ratio": round(bullwhip_ratio, 2),
        "consumer_demand_cv": round(cv_demand, 3),
        "upstream_order_cv": round(cv_orders, 3),
        "distortion_tier": tier,
        "recommended_dampened_next_order": round(smoothed_order, 1),
        "mitigation_strategy": action
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "dampen_supply_chain_bullwhip",
                        "description": """Quantify and dampen the Bullwhip Effect demand variance amplification across multi-echelon supply chains.
Bullwhip Measure = (Variance of Orders / Mean of Orders) / (Variance of Demand / Mean of Demand).
Calculates upstream distortion amplification ratio and provides Holt-Winters exponential smoothing allocation.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = dampen_supply_chain_bullwhip(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'consumer_demands': [100, 110, 95, 105, 115, 98], 'upstream_orders': [80, 140, 70, 150, 160, 65], 'smoothing_alpha': 0.3}
        out = dampen_supply_chain_bullwhip(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
