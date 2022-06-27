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
import pandas as pd


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        #TODO: initiate the stub
        stub = SafeEntry_pb2_grpc.SafeEntryStub(channel)

        #Main menu
        print("============MOH CLIENT============")
        print("1. Update infected locations")
        print("2. Infected History")
        print("3. Exit")
        print("============MOH CLIENT============")
        choice = input("Enter choice: ")
        print("\n")


        if choice == '1':
            print("=============================")
            print("Update Infections")
            print("=============================")
            num_grp = input("Enter number of infected cases: ")
            i = 0
            while(i<int(num_grp)):
                inputInfectedDetails(stub)
                i+=1
        elif choice =='2':
            print("=============================")
            print("History")
            print("=============================")
            InfectedHistory(stub)
        elif choice == '3':
            print("Goodbye...")
            quit()

def inputInfectedDetails(stub):
    # Ask for Details
    location = input("Enter Location: ")
    datetime = input("Enter Visit Date and Time (dd/mm/YYYY H:M): ")
    print(datetime)

    response = stub.Infected(SafeEntry_pb2.MOHRequest(location=location, datetime=datetime))
    return response


def InfectedHistory(stub):
    df_infected = pd.DataFrame(columns=['Location', 'Datetime'])
    response = stub.InfectedHistory(SafeEntry_pb2.MOHRequest())
    temp = response.res.split(',')
    row = []
    count = 0
    for i in temp:
        row.append(i)
        count+=1
        if count == 2:
            df_infected.loc[len(df_infected)] = row
            row = []
            count = 0

    print(df_infected)
    print("")

if __name__ == '__main__':
    logging.basicConfig()
    while True:
        run()
