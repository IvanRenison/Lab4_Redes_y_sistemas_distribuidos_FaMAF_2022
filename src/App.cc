#ifndef APP
#define APP

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class App: public cSimpleModule {
private:
    cMessage *sendMsgEvent;
    int packetsSent;
    int packetsReceived;
    cOutVector delayVector;
public:
    App();
    virtual ~App();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(App);

#endif /* APP */

App::App() {
}

App::~App() {
}

void App::initialize() {

    // If interArrivalTime for this node is higher than 0
    // initialize packet generator by scheduling sendMsgEvent
    if (par("interArrivalTime").doubleValue() != 0) {
        sendMsgEvent = new cMessage("sendEvent");
        scheduleAt(par("interArrivalTime"), sendMsgEvent);
    }

    // Initialize statistics
    packetsSent = 0;
    packetsReceived = 0;
    delayVector.setName("Delay");
}

void App::finish() {
    // Record statistics
    recordScalar("Sent packets", packetsSent);
    recordScalar("Received packets", packetsReceived);
}

void App::handleMessage(cMessage *msg) {

    // if msg is a sendMsgEvent, create and send new packet
    if (msg == sendMsgEvent) {
        // create new packet
        Packet *pkt = new Packet("packet",this->getParentModule()->getIndex());
        pkt->setByteLength(par("packetByteSize"));

        int source = this->getParentModule()->getIndex();
        pkt->setSource(source);

        int destination;
        do {
            destination = par("destination");
        }
        while (destination == source);
        pkt->setDestination(destination);

        // send to net layer
        send(pkt, "toNet$o");

        // Update stats
        packetsSent++;

        // compute the new departure time and schedule next sendMsgEvent
        simtime_t departureTime = simTime() + par("interArrivalTime");
        scheduleAt(departureTime, sendMsgEvent);

    }
    // else, msg is a packet from net layer
    else {
        // compute delay and record statistics
        simtime_t delay = simTime() - msg->getCreationTime();
        delayVector.record(delay);
        packetsReceived++;
        // delete msg
        delete (msg);
    }

}
