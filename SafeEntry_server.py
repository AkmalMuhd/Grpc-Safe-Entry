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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import SafeEntry_pb2
import SafeEntry_pb2_grpc
from os import path
import csv
import pandas as pd

df_entries = pd.DataFrame(columns=['Name', 'NRIC', 'Location', 'Datetime','Status'])

class SafeEntry(SafeEntry_pb2_grpc.SafeEntryServicer):

    header = ['Name', 'NRIC', 'Location', 'Datetime','Status']

    if path.exists("SafeEntries.csv") == False:
        print("Creating SafeEntries.csv")
        
        # Create can.csv and write header
        with open("SafeEntries.csv", 'w') as ff:
            writer = csv.writer(ff)
            writer.writerow(header)

    # def Add(self, request, context):
    #     return SafeEntry_pb2.Reply(res=request.x + request.y)

    # def Sub(self, request, context):
    #     return SafeEntry_pb2.Reply(res=request.x - request.y)

    # def Multiply(self, request, context):
    #     return SafeEntry_pb2.Reply(res=request.x * request.y)

    # def Divide(self, request, context):
    #     if request.y == 0:
    #         print("Error Y is 0!")
    #         return SafeEntry_pb2.Reply(res=-1)
    #     return SafeEntry_pb2.Reply(res=request.x / request.y)
    
    def CheckIn(self, request, context):
        with open("SafeEntries.csv", 'a', newline='') as f:
            writer = csv.writer(f)

            # Write to CSV
            row = [request.name, request.nric, request.location, request.datetime, "Checked-In"]
            writer.writerow(row)
            f.flush()

        # Add new row to df_entries Dataframe
        df_entries.loc[len(df_entries)] = row
        print(df_entries)
        print("")

        return SafeEntry_pb2.Reply(res=request.nric + " Checked in")

    def CheckOut(self, request, context):
        result = ""
        # iterate through dataframe
        for i in range(len(df_entries)):
            # check if nric and location is in dataframe
            if request.nric == df_entries.loc[i, "NRIC"] and request.location == df_entries.loc[i, "Location"]:
                # check if status is "Checked in"
                if df_entries.loc[i,"Status"] == "Checked-Out":
                    result = request.nric + "already checked out from " + request.location
                
                elif df_entries.loc[i,"Status"] == "Checked-In":
                    row = [request.name, request.nric, request.location, request.datetime, "Checked-Out"]
                    # add new row with status = Checked-out and check out timing
                    df_entries.loc[len(df_entries)] = row
                    print(df_entries)
                    result = request.nric + "Checked out"
            else:
                result = request.nric + "not checked-in into " + request.location

        return SafeEntry_pb2.Reply(res=result)

    def CheckInHistory(self, request, context):
        result = ""
        for i in range(len(df_entries)):
            print(i)
            if i == 0:
                result = df_entries.loc[i, "Name"] +","+ df_entries.loc[i, "NRIC"] +","+ df_entries.loc[i, "Location"] +","+ df_entries.loc[i, "Datetime"] +","+ df_entries.loc[i, "Status"]
            else:
                result =  result +","+ df_entries.loc[i, "Name"] +","+ df_entries.loc[i, "NRIC"] +","+ df_entries.loc[i, "Location"] +","+ df_entries.loc[i, "Datetime"] +","+ df_entries.loc[i, "Status"]
            # result.append(df_entries.loc[i, "Name"])
            # result.append(df_entries.loc[i, "NRIC"])
            # result.append(df_entries.loc[i, "Location"])
            # result.append(df_entries.loc[i, "Datetime"])
            # result.append(df_entries.loc[i, "Status"])
            print(result)
        return SafeEntry_pb2.Reply(res=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    SafeEntry_pb2_grpc.add_SafeEntryServicer_to_server(SafeEntry(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    print("Server is runnning")
    logging.basicConfig()
    serve()
