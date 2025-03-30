import pyshark


def answer_q2():

    print("QUESTION 2\n")

    # Load the .pcapng file and apply a CoAP display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="coap")

    resources = {}

    ########################### Process requests
    for pkt in packets:
        if not hasattr(pkt, "coap"):
            continue  # Skip non-CoAP packets

        coap_layer = pkt.coap

        if (
            int(coap_layer.code) == 1
            # check if it's a request to the local server
            and pkt.ip.dst == "134.102.218.18"
        ):

            if not hasattr(coap_layer, "opt_uri_path"):
                continue

            resource = coap_layer.opt_uri_path
            if resource not in resources:
                resources[resource] = {"confirmable": 0, "non-confirmable": 0}

            # check if it's a confirmable request
            if int(coap_layer.type) == 0:
                resources[resource]["confirmable"] += 1
            # check if it's a non confirmable request
            elif int(coap_layer.type) == 1:
                resources[resource]["non-confirmable"] += 1

    filtered_resources = {}
    for resource in resources:
        if resources[resource]["confirmable"] != 0 and resources[resource]["non-confirmable"] != 0:
            filtered_resources[resource] = resources[resource]

    print(filtered_resources)
    count = 0
    for resource in filtered_resources:
        if filtered_resources[resource]["confirmable"] == filtered_resources[resource]["non-confirmable"]:
            print(resource)
            count += 1
    print(count)
