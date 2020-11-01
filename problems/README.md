Howto obtain new hold setup JSON files?
- Login to moonboard.com
- Go to: https://www.moonboard.com/HoldSetups/Index
- Open the developer tools > Network > Response for GetHoldsetupHolds
- Paste the response to a temporary file
- Run ```jq -f filter.jq holds_tmp/holds_moonboard2016.tmp > holds_moonboard2016.json```