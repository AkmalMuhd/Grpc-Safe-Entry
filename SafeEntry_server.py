from concurrent import futures
import logging

import grpc
import SafeEntry_pb2
import SafeEntry_pb2_grpc
from os import path
import csv
import pandas as pd
from datetime import datetime

# Declare Dataframes to store SafeEntry entries and Infected Location separately 
df_entries = pd.DataFrame(columns=['Name', 'NRIC', 'Location', 'Datetime','Status'])
df_infected = pd.DataFrame(columns=['Location','Datetime', 'Status'])

class SafeEntry(SafeEntry_pb2_grpc.SafeEntryServicer):

    header = ['Name', 'NRIC', 'Location', 'Datetime','Status']
    infectedHeader = ['Location', 'Datetime','Status']

    if path.exists("SafeEntries.csv") == False:
        print("Creating SafeEntries.csv")
        
        # Create can.csv and write header
        with open("SafeEntries.csv", 'w', newline='') as ff:
            writer = csv.writer(ff)
            writer.writerow(header)

    # else, pull the data in the csv into the df
    else:  
        global df_entries
        df_entries = pd.read_csv("SafeEntries.csv")

    if path.exists("Infected.csv") == False:
        print("Creating Infected.csv")
        # Create can.csv and write header
        with open("Infected.csv", 'w', newline='') as ff:
            writer = csv.writer(ff)
            writer.writerow(infectedHeader)

    # else, pull the data in the csv into the df        
    else:  
        df_infected = pd.read_csv("Infected.csv")

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
        print(df_entries)
        # iterate through dataframe
        if len(df_entries) != 0:
            for i in reversed(range(len(df_entries))):
                
                # check if nric and location is in dataframe
                if request.nric.lower() == df_entries.loc[i, "NRIC"].lower() and request.location.lower() == df_entries.loc[i, "Location"].lower():
                    
                    # check if status is "Checked out"
                    if df_entries.loc[i,"Status"] == "Checked-Out":
                        result = request.nric + " already checked out from " + request.location
                        return SafeEntry_pb2.Reply(res=result)
                    
                    # check if status is "Checked in"
                    elif df_entries.loc[i,"Status"] == "Checked-In":
                        row = [request.name, request.nric, request.location, request.datetime, "Checked-Out"]
                        # add new row with status = Checked-out and check out timing
                        df_entries.loc[len(df_entries)] = row
                        result = request.nric + " Checked out"
                        with open("SafeEntries.csv", 'a', newline='') as f:
                            writer = csv.writer(f)

                            # Write to CSV
                            writer.writerow(row)
                            f.flush()
                        return SafeEntry_pb2.Reply(res=result)
        else:
            result = request.nric + " not checked-in into " + request.location
            return SafeEntry_pb2.Reply(res=result)

    def Infected(self, MOHrequest, context):
        with open("Infected.csv", 'a', newline='') as f:
            writer = csv.writer(f)

            # Write to CSV
            row = [MOHrequest.location, MOHrequest.datetime, "Infected"]
            writer.writerow(row)
            f.flush()

        # Add new row to df_entries Dataframe
        df_infected.loc[len(df_infected)] = row
        print(df_infected)
        print("")

        return SafeEntry_pb2.Reply(res=MOHrequest.location + " has been infected")

    def InfectedHistory(self, MOHrequest, context):
        df_infected = pd.read_csv("Infected.csv")
        result = ""
        for i in range(len(df_infected)):
            print(i)
            if i == 0:
                result = df_infected.loc[i, "Location"] +","+ df_infected.loc[i, "Datetime"]
            else:
                result =  result +","+df_infected.loc[i, "Location"] +","+ df_infected.loc[i, "Datetime"]
            print(result)
        return SafeEntry_pb2.Reply(res=result)

    def Notify(self, request, context):
        notification = ""
        nric = request.nric

        df_entries = pd.read_csv("SafeEntries.csv")
        df_infected = pd.read_csv("Infected.csv")

        user_entries = df_entries.loc[df_entries['NRIC'].str.lower() == nric.lower()]
        #Filter to Checked-In only to remove duplicates
        user_entries = user_entries.loc[user_entries['Status']=="Checked-In"]
        print(user_entries)
        for ind in user_entries.index:
            location = user_entries['Location'][ind].lower()
            user_datetime = datetime.strptime(user_entries['Datetime'][ind], '%d/%m/%Y %H:%M')
            infected = df_infected.loc[df_infected['Location'].str.lower() == location]
            for j in infected.index:
                infected_location = infected['Location'][j].lower()
                infected_datetime = datetime.strptime(infected['Datetime'][j], '%d/%m/%Y %H:%M')
                if infected_location == location:
                    delta = abs((infected_datetime - user_datetime).days)
                if (delta <= 14):
                    notification += "Possible exposure at " + location + " around " + user_datetime.strftime(
                        "%d/%m/%Y %H:%M") + "\n"
        if notification=="":
            notification="No recent exposure"
        return SafeEntry_pb2.Reply(res=notification)

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
