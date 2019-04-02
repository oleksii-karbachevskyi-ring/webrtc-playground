#include <stdlib.h>
#include <functional>
#include <iostream>
#include <string>
#include <mutex>
#include <thread>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/make_shared.hpp>

namespace asio = boost::asio;            // from <boost/asio.hpp>
using tcp = asio::ip::tcp;               // from <boost/asio/ip/tcp.hpp>

namespace beast = boost::beast;         // from <boost/beast.hpp>
namespace http  = beast::http;          // from <boost/beast/http.hpp>
namespace websocket = beast::websocket; // from <boost/beast/websocket.hpp>
namespace pt = boost::property_tree;

using namespace std;

mutex mtx;

class Communicator : public boost::enable_shared_from_this<Communicator> {
public:
    void SetSender(websocket::stream<tcp::socket>&& ws) {
        if (sender_ws) {
            beast::error_code err;
            sender_ws->close(websocket::close_code::none, err);
        }
        sender_ws = std::move(ws);
        AssignNextReadFromSender();
    }
    void SetReceiver(websocket::stream<tcp::socket>&& ws) {
        if (receiver_ws) {
            beast::error_code err;
            receiver_ws->close(websocket::close_code::none);
        }
        receiver_ws = std::move(ws);
        AssignNextReadFromReceiver();
    }
private:
    void AssignNextReadFromSender() {
        sender_ws->async_read(sender_buffer, [self = shared_from_this()]
            (error_code const& ec, std::size_t bytes_written) {
            if (!ec) {
                cout << "From sender:\n" << string((const char*)self->sender_buffer.data().data(), self->sender_buffer.data().size()) << endl;
                if (self->receiver_ws) {
                    self->receiver_ws->write(self->sender_buffer.data());
                }
                self->sender_buffer.consume(self->sender_buffer.size());
                self->AssignNextReadFromSender();
            }
        });
    }
    void AssignNextReadFromReceiver() {
        receiver_ws->async_read(receiver_buffer, [self = shared_from_this()]
            (error_code const& ec, std::size_t bytes_written) {
            if (!ec) {
                cout << "From receiver:\n" << string((const char*)self->receiver_buffer.data().data(), self->receiver_buffer.data().size()) << endl;
                if (self->sender_ws) {
                    self->sender_ws->write(self->receiver_buffer.data());
                }
                self->receiver_buffer.consume(self->receiver_buffer.size());
                self->AssignNextReadFromReceiver();
            }
        });
    }
    std::optional<websocket::stream<tcp::socket>> sender_ws;
    std::optional<websocket::stream<tcp::socket>> receiver_ws;
    beast::flat_buffer sender_buffer;
    beast::flat_buffer receiver_buffer;
};

int main(int argc, char* argv[])
{
    try
    {
        if (argc != 2)
        {
            std::cerr <<
                "Usage: wsserver <port>\n" <<
                "Example:\n" <<
                "    wsserver 8080\n";
            return EXIT_FAILURE;
        }
        auto const address = asio::ip::make_address("0.0.0.0");
        auto const port = static_cast<unsigned short>(std::atoi(argv[1]));

        // The io_context is required for all I/O
        asio::io_context ioc;
        boost::asio::executor_work_guard guard(ioc.get_executor());
        thread th([&ioc](){ ioc.run(); });


        // The acceptor receives incoming connections
        tcp::acceptor acceptor{ioc, {address, port}};

        auto c = boost::make_shared<Communicator>();
        //for (int clients_left = 2; clients_left >= 1; clients_left--) {
        for (;;) {
            boost::asio::ip::tcp::socket peer = acceptor.accept();
            // Accept succeeded.
            // Construct the stream by moving in the socket
            websocket::stream<tcp::socket> ws{std::move(peer)};

            // Accept the websocket handshake
            ws.accept();

            // This buffer will hold the incoming message
            beast::flat_buffer buffer;

            // Read a message
            ws.read(buffer);
            const void* p = buffer.data().data();
            size_t size = buffer.size();
            stringstream ss;
            ss << std::string((char*) p, size);
            cout << ss.str() << endl;
            pt::ptree pt;
            pt::read_json(ss, pt);
            string who = pt.get("who", "none");
            if (who == "sender") {
                cout << "Got Sender" << endl;
                c->SetSender(move(ws));
            } else if (who == "receiver") {
                cout << "Got Receiver" << endl;
                c->SetReceiver(move(ws));
            }
        }
        th.join();
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
    return 0;
}
