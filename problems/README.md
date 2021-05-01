Howto obtain new hold setup JSON files?
# How to download new hold setups?

- Login to moonboard.com
- Go to: https://www.moonboard.com/HoldSetups/Index
- Open the developer tools > Network > Response for GetHoldsetupHolds
- Paste the response to a temporary file
- Run ```python3 problems/create_hold_json.py && cat HoldSetup.txt | jq > problems/HoldSetup.json ```
