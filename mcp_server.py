import sys, json
from client import BondDurationConvexity

calc = BondDurationConvexity()

def handle_jsonrpc(line):
    global calc
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-bond-convexity-modified-duration-calculator-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "evaluate_bond", "description": "Calculate bond price, duration and convexity.", "inputSchema": {"type": "object", "properties": {"face_value": {"type": "number"}, "coupon_rate": {"type": "number"}, "ytm": {"type": "number"}, "maturity_years": {"type": "integer"}}, "required": ["face_value", "coupon_rate", "ytm", "maturity_years"]}},
                {"name": "benchmark_bond_analytics", "description": "Run bond analytics benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "evaluate_bond":
                res = calc.evaluate(args.get("face_value"), args.get("coupon_rate"), args.get("ytm"), args.get("maturity_years"))
            elif tool == "benchmark_bond_analytics":
                res = calc.benchmark_bond_analytics()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
