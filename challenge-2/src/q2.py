import pyshark

def answer_q2():
    print("QUESTION 2\n")

    # load the file and apply the filter
    # coap.code filters only GET requests
    # ip.dst filters requests to the public coap.me server
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", 
        display_filter="coap and coap.code==1 and ip.dst==134.102.218.18")

    resources = {}

    for pkt in packets:
        # skip non coap packets
        if not hasattr(pkt, "coap"):
            continue

        coap_layer = pkt.coap

        # check if it has the resource path
        if not hasattr(coap_layer, "opt_uri_path"):
            continue

        # get the resource and if needed initialize the data structure
        # saving the number of confirmable and non-confirmable requests
        # per resource
        resource = coap_layer.opt_uri_path
        if resource not in resources:
            resources[resource] = {"confirmable": 0, "non-confirmable": 0}

        # check if it's a confirmable request and update the counter
        if int(coap_layer.type) == 0:
            resources[resource]["confirmable"] += 1
        # check if it's a non confirmable request and update the counter
        elif int(coap_layer.type) == 1:
            resources[resource]["non-confirmable"] += 1

    # remove resources where at least one of the number of confirmable or
    # non confirmable resources is zero
    filtered_resources = {}
    for resource in resources:
        if resources[resource]["confirmable"] != 0 and resources[resource]["non-confirmable"] != 0:
            filtered_resources[resource] = resources[resource]

    print(filtered_resources)

    # count the resources that satisfy the conditions
    count = 0
    for resource in filtered_resources:
        if filtered_resources[resource]["confirmable"] == filtered_resources[resource]["non-confirmable"]:
            print(resource)
            count += 1
    print(count)

if __name__ == "__main__":
    answer_q2()
