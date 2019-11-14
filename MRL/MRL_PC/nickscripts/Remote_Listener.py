remoteAdapterB = Runtime.createAndStart("RemoteAdapterB","RemoteAdapter")
# Change to the ip address of the remote host
remoteAdapterB.connect("tcp://192.168.1.31:6767")