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
import argparse
from os import path
import csv

df_entries = pd.DataFrame(columns=['Name', 'NRIC', 'Location', 'Datetime','Status'])

def run(name,nric):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        #Creating personal SafeEntry records file for clients
        #If csv does not exist, create it
        if not path.exists("SafeEntry_" + nric.lower() + ".csv"):
            print("Creating SafeEntry_" + nric.lower() + ".csv")
            # Create can.csv and write header
            with open("SafeEntry_" + nric.lower() + ".csv", 'w', newline='') as ff:
                header = ['Name', 'NRIC', 'Location', 'Datetime', 'Status']
                writer = csv.writer(ff)
                writer.writerow(header)

        else: #else, pull the data in the csv into the df
            df_entries = pd.read_csv("SafeEntry_" + nric.lower() + ".csv")
            #print(df_entries)

        #TODO: initiate the stub
        stub = SafeEntry_pb2_grpc.SafeEntryStub(channel)

        #Main menu
        print("=============================")
        print("1. Individual Check-in")
        print("2. Group Check-in")
        print("3. Individual Check-out")
        print("4. Group Check-out")
        print("5. History")
        print("6. Notifications")
        print("7. End")
        print("=============================")
        choice = input("Enter choice: ")
        print("\n")

        if choice == '1':
            print("=============================")
            print("Individual Check-in")
            print("=============================")
            i = 0
            inputDetailsCheckIn(stub,name, nric, i)

        elif choice == '2':
            print("=============================")
            print("Group Check-in")
            print("=============================")
            num_grp = input("Enter number of people: ")
            i = 0
            while(i<int(num_grp)):
                inputDetailsCheckIn(stub,name,nric, i)
                i+=1

        elif choice =='3':
            print("=============================")
            print("Individual Check-out")
            print("=============================")
            i=0
            inputDetailsCheckOut(stub,name,nric, i)

        elif choice =='4':
            print("=============================")
            print("Group Check-out")
            print("=============================")
            num_grp = input("Enter number of people: ")
            i = 0
            while(i<int(num_grp)):
                inputDetailsCheckOut(stub,name,nric, i)
                i+=1
            

        elif choice =='5':
            print("=============================")
            print("History")
            print("=============================")
            history(stub)

        elif choice =='6':
            print("=============================")
            print("Notifications")
            print("=============================")
            notify(stub, nric)
            print("=============================")

        elif choice == '7':
            print("Goodbye...")
            quit()

def inputDetailsCheckIn(stub,username, userNRIC, i):
    # Ask for Details
    if i==0:
        name=username
        print("Name: "+username)
        nric = userNRIC
        print("NRIC: " + userNRIC)
        location = input("Enter Location: ")
        datetime = getCurrentDatetime()

    else:
        name = input("Enter member "+str(i)+" name: ")
        nric = input("Enter member "+str(i)+" NRIC: ")
        location = input("Enter member "+str(i)+" Location: ")
        datetime = getCurrentDatetime()

    with open("SafeEntry_" + nric.lower() + ".csv", 'a', newline='') as f:
        writer = csv.writer(f)

        # Write to CSV
        row = [name, nric, location, datetime, "Checked-In"]
        writer.writerow(row)
        f.flush()

    # Add new row to df_entries Dataframe
    df_entries.loc[len(df_entries)] = row
    print(df_entries)
    print("")

    response = stub.CheckIn(SafeEntry_pb2.Request(name=name, nric=nric, location=location, datetime=datetime))
    print(nric + " checked in")
    print("")

def inputDetailsCheckOut(stub,username, userNRIC, i):
    # Ask for Details
    if i == 0:
        name = username
        print("Name: " + username)
        nric = userNRIC
        print("NRIC: " + userNRIC)
        location = input("Enter Location: ")
        datetime = getCurrentDatetime()

    else:
        name = input("Enter member " + str(i) + " name: ")
        nric = input("Enter member " + str(i) + " NRIC: ")
        location = input("Enter member " + str(i) + " Location: ")
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

def notify(stub,nric):
    response = stub.Notify(SafeEntry_pb2.Request(nric=nric))
    print(response.res)

def getCurrentDatetime():
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    print("Current datetime: ", dt_string)
    return dt_string

if __name__ == '__main__':
    logging.basicConfig()
    name = input("Name: ")
    nric = input("NRIC: ")
    while True:
        run(name, nric)
