from __future__ import print_function
import logging
import grpc
import SafeEntry_pb2
import SafeEntry_pb2_grpc
import pandas as pd


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        # Initiate the stub
        stub = SafeEntry_pb2_grpc.SafeEntryStub(channel)

        # Main menu
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
