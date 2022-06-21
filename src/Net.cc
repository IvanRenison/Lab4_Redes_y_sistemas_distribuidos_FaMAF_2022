#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>
#include <time.h>

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    // Topology
    unsigned int nodeCount {0};
    bool topologyRecognized {false};

    // Queue of packets
    cQueue buffer;

    // Functions
    void sendPacket(Packet *pkt);
    void sendPacketsInBuffer();
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

#define NORMAL_KIND 0
#define RECOGNITION_KIND 2
#define RECOGNITION_OUTGATE 0

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    // Set seed for rand
    srand(time(NULL));

    // Send recognition packet for knowing the size of the ring
    Packet *recognitionPacket = new Packet();
    recognitionPacket->setKind(2);
    recognitionPacket->setByteLength(RECOGNITION_KIND);
    recognitionPacket->setHopCount(0);
    recognitionPacket->setSource(this->getParentModule()->getIndex());
    recognitionPacket->setDestination(this->getParentModule()->getIndex());

    send(recognitionPacket, "toLnk$o", RECOGNITION_OUTGATE);
}

void Net::finish() {
}

void Net::sendPacket(Packet *pkt) {
    assert(pkt->getKind() == NORMAL_KIND);

    int destination = pkt->getDestination();
    int source = this->getParentModule()->getIndex();

    int antiClockwiseDistance = (destination - source) % nodeCount;
    int clockwiseDistance = nodeCount - antiClockwiseDistance;

    int out;

    // Checking if the shortest path is clockwise or counter clockwise
    if (antiClockwiseDistance > clockwiseDistance) {
        // Clock-wise is the best route
        out = 0;
    }
    else if (antiClockwiseDistance < clockwiseDistance) {
        // Counter-clock-wise is the best route
        out = 1;
    }
    else {
        // Either route is the best, choose randomly
        out = rand() % 2;
    }

    send(pkt, "toLnk$o", out);
}

void Net::sendPacketsInBuffer() {
    while (!buffer.isEmpty()) {
        Packet* pkt = (Packet*) buffer.pop();
        sendPacket(pkt);
    }
}

void Net::handleMessage(cMessage *msg) {
    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;

    if (pkt->getKind() == RECOGNITION_KIND
            && pkt->getDestination() == this->getParentModule()->getIndex()) {
        // It's a recognitionMessage with the amount of nodes in the network
        nodeCount = pkt->getHopCount() + 1;
        topologyRecognized = true;
        delete (pkt);
    }
    else if (pkt->getDestination() == this->getParentModule()->getIndex()) {
        // If this node is the final destination, send to App
        send(pkt, "toApp$o");
    } else if (pkt->arrivedOn("toLnk$i")) {
        // The packet is from other node
        // Send to the other gate 
        // (note that this is executed for every kind of packet)

        if (pkt->getKind() == RECOGNITION_KIND) {
            pkt->setHopCount(pkt->getHopCount() + 1);
        }

        if (pkt->arrivedOn("toLnk$i", 0)) {
            send(pkt, "toLnk$o", 1);
        }
        else {
            send(pkt, "toLnk$o", 0);
        }
    } else {
        // It's a packet from the app
        assert(pkt->arrivedOn("toApp$i"));

        buffer.insert(pkt);

        if (topologyRecognized) {
            sendPacketsInBuffer();
        }
    }
}
