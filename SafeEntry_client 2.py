# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
#TODO: import _pb2 and _pb2_grpc
import SafeEntry_pb2
import SafeEntry_pb2_grpc
from datetime import datetime
end = 0


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        #TODO: initiate the stub
        stub = SafeEntry_pb2_grpc.SafeEntryStub(channel)

        #Main menu
        print("=============================")
        print("1. Individual Check-in")
        print("2. Group Check-in")
        print("3. End")
        print("=============================")
        choice = input("Enter choice: ")
        print("\n")



        if choice == '1':
            print("=============================")
            print("Individual Check-in")
            print("=============================")
            inputDetails(stub)

        elif choice == '2':
            print("=============================")
            print("Group Check-in")
            print("=============================")
            num_grp = input("Enter number of people: ")
            i = 0
            while(i<int(num_grp)):
                inputDetails(stub)
                i+=1
        elif choice == '3':
            print("Goodbye...")
            end += 1

        
        # print("Name is: "+ response.res)

        # response = stub.Add(SafeEntry_pb2.Request(x=5, y=6))
        # print("The result of Add Function is: " + str(response.res))

        # #TODO: invoke the Sub() procedure and print the result
        # response = stub.Sub(SafeEntry_pb2.Request(x=5, y=6))
        # print("The result of Sub Function is: " + str(response.res))

        # #TODO: invoke the Multipy() procedure and print the result
        # response = stub.Multiply(SafeEntry_pb2.Request(x=5, y=6))
        # print("The result of Multiply Function is: " + str(response.res))

        # #TODO: invoke the Divide() procedure and print the result
        # response = stub.Divide(SafeEntry_pb2.Request(x=5, y=0))
        # print("The result of Divide Function is: " + str(response.res))

def inputDetails(stub):
    # Ask for Details
    name = input("Enter name: ")
    nric = input("Enter NRIC: ")
    location = input("Enter Location: ")
    datetime = getCurrentDatetime()

    response = stub.CheckIn(SafeEntry_pb2.Request(name=name, nric=nric, location=location, datetime=datetime))


def getCurrentDatetime():
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Current datetime: ", dt_string)
    return dt_string

if __name__ == '__main__':
    logging.basicConfig()
    while(end==0):
        run()
