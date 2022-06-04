#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>
#include <time.h>

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    unsigned int nodeCount {0};
    bool topologyRecognized {false};

    void sendMessage(Packet *pkt);
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

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    srand(time(NULL));
    Packet *recognitionPacket = new Packet();
    recognitionPacket->setKind(2);
    recognitionPacket->setByteLength(1);
    recognitionPacket->setHopCount(0);
    recognitionPacket->setSource(this->getParentModule()->getIndex());
    recognitionPacket->setDestination(this->getParentModule()->getIndex());
    handleMessage(recognitionPacket);
}

void Net::finish() {
}

void Net::sendMessage(Packet *pkt) {
    int out = 0;

    if (pkt->getKind() == 2) {
        // It's a recognitionMessage
        int hopCount = pkt->getHopCount() + 1;
        pkt->setHopCount(hopCount);
    }
    if (topologyRecognized) {
        // Checking if the shortest path is clockwise or counter clockwise
        int source = this->getParentModule()->getIndex();
        int destination = pkt->getDestination();
        int distance = abs(source - destination);
        if (distance < nodeCount / 2 && source < destination) {
            // Counter-clock-wise is the best route
            out = 1;
        } else if (distance == nodeCount / 2) {
            // Either route is the best, choose randomly
            out = rand() % 2;
        }
    }

    send(pkt, "toLnk$o", out);
}

void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;

    if (pkt->getKind() == 2 && pkt->getHopCount() > 0 
    && pkt->getDestination() == this->getParentModule()->getIndex()) {
        // It's a recognitionMessage with the amount of nodes in the network
        nodeCount = pkt->getHopCount();
        topologyRecognized = true;
        delete (pkt);
    } else if (pkt->getDestination() == this->getParentModule()->getIndex() && pkt->getKind() != 2) {
        // If this node is the final destination, send to App
        send(msg, "toApp$o");
    } else {
        // Where should the message be sent
        sendMessage(pkt);
    }
}
