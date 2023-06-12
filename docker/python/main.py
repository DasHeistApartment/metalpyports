from kubernetes import client, config, watch
import portforwardlib

def main():
    config.load_incluster_config()
    v1_core = client.CoreV1Api()
    w = watch.Watch()
    for event in w.stream(v1_core.list_service_for_all_namespaces):
        print("Service: %s %s" % (event['type'], event['object'].metadata.name))
        if (event['object'].spec.type != 'LoadBalancer'):
            continue
        if (event['type'] == 'ADDED'):
            annotations = dict(event['object'].metadata.annotations)
            for key, value in annotations.items():
                if (key == 'metalpyports.dasheistapartment/forward'):
                    for port in event['object'].spec.ports:
                        for ingress in event['object'].status.load_balancer.ingress:
                            ip = ingress.ip
                            source = port.port
                            target = port.port
                            print("Forwarding port %d to port %d on %s..." % (source, target, ip))
                            result = portforwardlib.forwardPort(eport = source, iport = target, router = None, protocol = port.protocol, lanip = ip, disable = False, time = 0, description = "MetalPyPorts", verbose = True)
                            print(result)
                            if not result: print("Something went wrong forwarding port %d to port %d on %s. Maybe the forward already exists?" % (source, target, ip))

if __name__ == '__main__':
    main()