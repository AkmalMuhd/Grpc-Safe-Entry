# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import SafeEntry_pb2 as SafeEntry__pb2


class SafeEntryStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckIn = channel.unary_unary(
                '/SafeEntry.SafeEntry/CheckIn',
                request_serializer=SafeEntry__pb2.Request.SerializeToString,
                response_deserializer=SafeEntry__pb2.Reply.FromString,
                )
        self.CheckOut = channel.unary_unary(
                '/SafeEntry.SafeEntry/CheckOut',
                request_serializer=SafeEntry__pb2.Request.SerializeToString,
                response_deserializer=SafeEntry__pb2.Reply.FromString,
                )
        self.CheckInHistory = channel.unary_unary(
                '/SafeEntry.SafeEntry/CheckInHistory',
                request_serializer=SafeEntry__pb2.Request.SerializeToString,
                response_deserializer=SafeEntry__pb2.Reply.FromString,
                )
        self.Infected = channel.unary_unary(
                '/SafeEntry.SafeEntry/Infected',
                request_serializer=SafeEntry__pb2.MOHRequest.SerializeToString,
                response_deserializer=SafeEntry__pb2.Reply.FromString,
                )
        self.InfectedHistory = channel.unary_unary(
                '/SafeEntry.SafeEntry/InfectedHistory',
                request_serializer=SafeEntry__pb2.MOHRequest.SerializeToString,
                response_deserializer=SafeEntry__pb2.Reply.FromString,
                )


class SafeEntryServicer(object):
    """The greeting service definition.
    """

    def CheckIn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckOut(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckInHistory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Infected(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InfectedHistory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SafeEntryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CheckIn': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckIn,
                    request_deserializer=SafeEntry__pb2.Request.FromString,
                    response_serializer=SafeEntry__pb2.Reply.SerializeToString,
            ),
            'CheckOut': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckOut,
                    request_deserializer=SafeEntry__pb2.Request.FromString,
                    response_serializer=SafeEntry__pb2.Reply.SerializeToString,
            ),
            'CheckInHistory': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckInHistory,
                    request_deserializer=SafeEntry__pb2.Request.FromString,
                    response_serializer=SafeEntry__pb2.Reply.SerializeToString,
            ),
            'Infected': grpc.unary_unary_rpc_method_handler(
                    servicer.Infected,
                    request_deserializer=SafeEntry__pb2.MOHRequest.FromString,
                    response_serializer=SafeEntry__pb2.Reply.SerializeToString,
            ),
            'InfectedHistory': grpc.unary_unary_rpc_method_handler(
                    servicer.InfectedHistory,
                    request_deserializer=SafeEntry__pb2.MOHRequest.FromString,
                    response_serializer=SafeEntry__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SafeEntry.SafeEntry', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SafeEntry(object):
    """The greeting service definition.
    """

    @staticmethod
    def CheckIn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SafeEntry.SafeEntry/CheckIn',
            SafeEntry__pb2.Request.SerializeToString,
            SafeEntry__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckOut(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SafeEntry.SafeEntry/CheckOut',
            SafeEntry__pb2.Request.SerializeToString,
            SafeEntry__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckInHistory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SafeEntry.SafeEntry/CheckInHistory',
            SafeEntry__pb2.Request.SerializeToString,
            SafeEntry__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Infected(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SafeEntry.SafeEntry/Infected',
            SafeEntry__pb2.MOHRequest.SerializeToString,
            SafeEntry__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InfectedHistory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SafeEntry.SafeEntry/InfectedHistory',
            SafeEntry__pb2.MOHRequest.SerializeToString,
            SafeEntry__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)