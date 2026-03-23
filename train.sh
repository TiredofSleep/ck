#!/bin/bash
# CK Training Script
# Usage: ./train.sh [model] [rounds]
# Example: ./train.sh phi4 500
#
# Requires: CK running at localhost:7777, Ollama running with model pulled
#
# (c) 2026 Brayden Sanders / 7Site LLC

MODEL=${1:-llama3.2}
ROUNDS=${2:-100}
API="http://localhost:7777"

echo "CK Training: $MODEL x $ROUNDS rounds"
echo ""

# Check CK is alive
if ! curl -sf "$API/health" > /dev/null 2>&1; then
    echo "ERROR: CK not running. Start with: python targets/ck_desktop/ck_boot_api.py"
    exit 1
fi

# Check Ollama is alive
if ! curl -sf "http://localhost:11434/api/tags" > /dev/null 2>&1; then
    echo "ERROR: Ollama not running. Start with: ollama serve"
    exit 1
fi

# Start eating
echo "Starting eat: $MODEL x $ROUNDS rounds..."
curl -s -X POST "$API/eat" \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$MODEL\", \"rounds\": $ROUNDS}" | python3 -m json.tool 2>/dev/null || echo "Eat started"

echo ""
echo "Monitoring progress (Ctrl+C to stop watching)..."
echo ""

# Monitor
while true; do
    STATUS=$(curl -sf "$API/eat/status" 2>/dev/null)
    if [ -z "$STATUS" ]; then
        echo "CK not responding"
        sleep 10
        continue
    fi

    DONE=$(echo "$STATUS" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('rounds_complete',0))" 2>/dev/null)
    TOTAL=$(echo "$STATUS" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('total_rounds',0))" 2>/dev/null)
    OLFA=$(echo "$STATUS" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('olfactory_library_size',0))" 2>/dev/null)
    RUNNING=$(echo "$STATUS" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('running',False))" 2>/dev/null)

    STATE=$(curl -sf "$API/state" 2>/dev/null)
    COH=$(echo "$STATE" | python3 -c "import sys,json;d=json.load(sys.stdin);print('%.3f' % d.get('coherence',0))" 2>/dev/null)

    echo "[$DONE/$TOTAL] olfa=$OLFA coh=$COH"

    if [ "$RUNNING" = "False" ] && [ "$DONE" -ge "$TOTAL" ] 2>/dev/null; then
        echo ""
        echo "TRAINING COMPLETE"

        # Test math
        echo ""
        echo "Math test:"
        for EXPR in "2+2" "7*7" "x+3=7"; do
            RESULT=$(curl -sf -X POST "$API/chat" \
                -H "Content-Type: application/json" \
                -d "{\"text\": \"$EXPR\"}" 2>/dev/null | \
                python3 -c "import sys,json;print(json.load(sys.stdin).get('text','')[:60])" 2>/dev/null)
            echo "  $EXPR => $RESULT"
        done

        # Voice test
        echo ""
        echo "Voice test:"
        VOICE=$(curl -sf -X POST "$API/chat" \
            -H "Content-Type: application/json" \
            -d '{"text": "What have you learned?"}' 2>/dev/null | \
            python3 -c "import sys,json;d=json.load(sys.stdin);print('[%s|%.2f] %s' % (d.get('source','?'),d.get('coherence',0),d.get('text','')[:60]))" 2>/dev/null)
        echo "  $VOICE"

        break
    fi

    sleep 30
done
