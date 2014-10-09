from __future__ import absolute_import, division, print_function

import os

from tls.hello_message import ClientHello, ProtocolVersion

from tls.message import Handshake, HandshakeType

from tls.record import TLSPlaintext, ContentType


class ClientTLS(object):
    """
    The user will create this and pass to it the things needed to create a
    ClientHello object.
    """

    def __init__(self, major_version, minor_version, gmt_unix_time, session_id='', cipher_suites, compression_methods, extensions=''):
        self.major_version = major_version
        self.minor_version = minor_version
        self.gmt_unix_time = gmt_unix_time      # TODO:Figure out how togenerate this
        self.random_bytes = os.urandom(28)
        self.session_id = session_id            # TODO: How to we generate a session ID?
        self.cipher_suites = cipher_suites
        self.compression_methods = compression_methods
        self.extensions = extensions


    def start(self, write_to_wire_callback, wire_close_callback, verify_callback=None):
        """
        First, this creates a ClientHello message and writes it to the wire.
        Then, it creates a Connection object and passes to it the ClientHello
        messsage to extract details of the connection for further use in the
        handshake. Returns that Connection object.
        """
        # Create a ClientHello message.
        client_hello = ClientHello(
            client_version=ProtocolVersion(
                major=self.major_version,
                minor=self.minor_version
            ),
            random=Random(
                gmt_unix_time=self.gmt_unix_time,
                random_bytes=self.random_bytes
            ),
            session_id=self.session_id,
            cipher_suites=self.cipher_suites,
            compression_methods=self.compression_methods,
            extensions=self.extensions,
        )

        client_hello_as_bytes = client_hello.as_bytes()

        # create a handshake struct with this clienthello
        handshake = Handshake(
            msg_type=HandshakeType.CLIENT_HELLO,
            length=len(client_hello_as_bytes),
            body=client_hello
        )

        # Create a TLSPlaintext record for this Handshake struct
        tls_plaintext_record = TLSPlaintext(
            type=ContentType.HANDSHAKE,
            version=ProtocolVersion(
                major=self.major_version,
                minor=self.minor_version
            ),
            fragment=handshake.as_bytes()   # XXX: Implement fragmentation mechanism here.
        )


        # Write this to wire.
        write_to_wire_callback(tls_plaintext_record.as_bytes())

        # Create a Connection object and pass the ClientHello-Handshake struct to it.
        conn = Connection(write_to_wire_callback)
        conn.handshake_msg_store[handshake.msg_type] = handshake
        return conn



class ServerTLS(object):
    """
    The user will create this and pass to it the things needed to create a
    ServerHello object.
    """
    def __init__(self):
        pass

    def start(self, write_to_wire_callback, verify_callback=None):
        conn = Connection(write_to_wire_callback)









class Connection(object):

    def __init__(self, write_to_wire_callback):
        self.write_to_wire_callback = write_to_wire_callback
        self.handshake_msg_store = {}

    def structure_bytes_from_wire(self, input_bytes):
        """
        Receive data and build a structure out of it.
        """
        # TODO: Buffering of fragmented messages goes here.

        tls_plaintext_record = parse_tls_plaintext(input_bytes)
        if tls_plaintext_record.type == ContentType.HANDSHAKE:
            handshake_struct = parse_handshake_struct(tls_plaintext_record.fragment)
            self.handshake_msg_store[handshake_struct.msg_type] = handshake_struct


    def construct_bytes_from_application_and_write_to_wire(self, output):
        """
        Encrypt application data and send. This is only useful in APP_DATA state.
        """
        encrypted_output = encrypt_output_bytes_with_negotiated_cipher_suite
        self.write_to_wire_callback(encrypted_output)






