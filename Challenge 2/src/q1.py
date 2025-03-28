import pyshark


def answer_q1():
    print("QUESTION 1")
    # Load the .pcapng file and apply a CoAP display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="coap")

    # Store requests by Message ID (MID)
    requests = {}
    failed_responses = []

    # Process packets
    for pkt in packets:
        if not hasattr(pkt, "coap"):
            continue  # Skip non-CoAP packets

        coap_layer = pkt.coap

        # Check if it's a Confirmable PUT request
        if coap_layer.type == "0" and coap_layer.code == "3":
            requests[coap_layer.mid] = pkt  # Store PUT request by MID

        # Check if it's an error response (4.xx or 5.xx)
        elif int(coap_layer.code.split(".")[0]) in [4, 5]:
            if coap_layer.mid in requests:  # Match with the stored request
                req_pkt = requests[coap_layer.mid]

                # Ensure response is from localhost (127.0.0.1 or ::1)
                if pkt.ip.src in ["127.0.0.1", "::1"]:
                    failed_responses.append((req_pkt, pkt))

    # Display failed transactions
    for req, resp in failed_responses:
        print("==== Failed CoAP PUT Request ====")
        print(
            f"Time: {req.sniff_time}, MID: {req.coap.mid}, Source: {req.ip.src} → {req.ip.dst}"
        )
        print(
            f"Request Payload: {req.coap.payload if hasattr(req.coap, 'payload') else 'N/A'}\n"
        )

        print("==== CoAP Error Response ====")
        print(
            f"Time: {resp.sniff_time}, MID: {resp.coap.mid}, Response Code: {resp.coap.code}, Source: {resp.ip.src} → {resp.ip.dst}"
        )
        print(
            f"Response Payload: {resp.coap.payload if hasattr(resp.coap, 'payload') else 'N/A'}\n"
        )

        print("=" * 50 + "\n")
