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
import SafeEntry_pb2
import SafeEntry_pb2_grpc
from datetime import datetime
import pandas as pd
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
        print("3. Individual Check-out")
        print("4. Group Check-out")
        print("5. History")
        print("6. End")
        print("=============================")
        choice = input("Enter choice: ")
        print("\n")

        if choice == '1':
            print("=============================")
            print("Individual Check-in")
            print("=============================")
            inputDetailsCheckIn(stub)

        elif choice == '2':
            print("=============================")
            print("Group Check-in")
            print("=============================")
            num_grp = input("Enter number of people: ")
            i = 0
            while(i<int(num_grp)):
                inputDetailsCheckIn(stub)
                i+=1

        elif choice =='3':
            print("=============================")
            print("Individual Check-out")
            print("=============================")
            inputDetailsCheckOut(stub)

        elif choice =='4':
            print("=============================")
            print("Group Check-out")
            print("=============================")
            num_grp = input("Enter number of people: ")
            i = 0
            while(i<int(num_grp)):
                inputDetailsCheckOut(stub)
                i+=1
            

        elif choice =='5':
            print("=============================")
            print("History")
            print("=============================")
            history(stub)

        elif choice == '6':
            print("Goodbye...")
            end += 1

def inputDetailsCheckIn(stub):
    # Ask for Details
    name = input("Enter name: ")
    nric = input("Enter NRIC: ")
    location = input("Enter Location: ")
    datetime = getCurrentDatetime()

    response = stub.CheckIn(SafeEntry_pb2.Request(name=name, nric=nric, location=location, datetime=datetime))
    print(nric + " checked in")
    print("")

def inputDetailsCheckOut(stub):
    # Ask for Details
    name = input("Enter name: ")
    nric = input("Enter NRIC: ")
    location = input("Enter Location: ")
    datetime = getCurrentDatetime()

    response = stub.CheckOut(SafeEntry_pb2.Request(name=name, nric=nric, location=location, datetime=datetime))
    print(nric + " checked out")
    print("")

def history(stub):
    df_entries = pd.DataFrame(columns=['Name', 'NRIC', 'Location', 'Datetime','Status'])
    response = stub.CheckInHistory(SafeEntry_pb2.Request())
    temp = response.res.split(',')
    row = []
    count = 0
    for i in temp:
        row.append(i)
        count+=1
        if count == 5:
            df_entries.loc[len(df_entries)] = row
            row = []
            count = 0

    print(df_entries)
    print("")

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
