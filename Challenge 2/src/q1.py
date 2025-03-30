import pyshark


def answer_q1():
    print("QUESTION 1\n")

    # Load the .pcapng file and apply a CoAP display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="coap")

    # Store requests by Token
    requests = {}
    failed_responses = []

    ########################### Process requests
    for pkt in packets:
        if not hasattr(pkt, "coap"):
            continue  # Skip non-CoAP packets

        coap_layer = pkt.coap

        # Check if the packet has a Token
        if not hasattr(coap_layer, "token"):
            continue

        token = coap_layer.token

        if (
            # check if it's a confirmable request
            int(coap_layer.type) == 0
            # check if it's a PUT request
            and int(coap_layer.code) == 3
            # check if it's a request to the local server
            and pkt.ip.dst == "127.0.0.1"
        ):
            # store the request by its coap token
            requests[token] = pkt

    ########################### Process responses
    for pkt in packets:
        if not hasattr(pkt, "coap"):
            continue  # Skip non-CoAP packets

        coap_layer = pkt.coap

        # Check if the packet has a Token
        if not hasattr(coap_layer, "token"):
            continue

        token = coap_layer.token

        # Check if it's an error response (4.xx or 5.xx)
        if int(coap_layer.code) >= 128 and int(coap_layer.code) <= 165:
            # check if the token is present in the requests keys
            if token in requests:
                req_pkt = requests[token]

                # check if it's a response from the local server
                if pkt.ip.src == "127.0.0.1":
                    failed_responses.append((req_pkt, pkt))

    # Display failed transactions
    for req, resp in failed_responses:
        print("==== Failed CoAP PUT Request ====")
        print(
            f"Time: {req.sniff_time}, TOKEN: {req.coap.token}, Source: {req.ip.src} → {req.ip.dst}"
        )
        print(
            f"Request Payload: {req.coap.payload if hasattr(req.coap, 'payload') else 'N/A'}\n"
        )

        print("==== CoAP Error Response ====")
        print(
            f"Time: {resp.sniff_time}, TOKEN: {resp.coap.token}, Response Code: {resp.coap.code}, Source: {resp.ip.src} → {resp.ip.dst}"
        )
        print(
            f"Response Payload: {resp.coap.payload if hasattr(resp.coap, 'payload') else 'N/A'}\n"
        )

        print("=" * 50 + "\n")

    print(len(failed_responses))
