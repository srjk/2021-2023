#read the command list from the DB and put them in the list

import psycopg2
import json
import pandas as pd


def readdbcommands(input_data):
    print(f"i am inside readdbcommands now {input_data}")

    vendor=input_data["vendor"]
    cnf_type=input_data["cnf_type"]
    deploy_env=input_data["deploy_env"]
    operation=input_data["operation"]
    namespace=input_data["cnf_namespace"]

    print(f"invendor ={vendor}")
    print(f"cnftype is {cnf_type}")
    print(f"deploy_env is {deploy_env}")
    try:
    # establishing the connection
        conn = psycopg2.connect(
            database="provision",
            user='postgres',
            password='FZYb62D26J',
            host='k8s-cyswy001-iborcpos-659318ab00-deb12c900821a95d.elb.us-east-2.amazonaws.com',
            port= '80')

        cursor=conn.cursor()
    except Exception as e:
        print(f"unable to establist connection to db {e}")
        #Select query from db
    try:
        cursor.execute(f"""SELECT * FROM tbl_nflcm_nf_cmd WHERE tbl_nflcm_nf_cmd.vendor='{vendor}' AND tbl_nflcm_nf_cmd.cnf='{cnf_type}' AND tbl_nflcm_nf_cmd.deploy_env='{deploy_env}' AND tbl_nflcm_nf_cmd.operation='{operation}'""")
    
    except Exception as e:
        print(f"unable to excute query {e}")
    try:
        commandlist=[]
        kubectllist=[]
        record = [item for item in cursor.fetchall()]
        #print(f"records are {record}")
        count = cursor.rowcount
        #print(f"row count is {count}")
        for row in record:
            print(f"kubectl record is {row[5]}\n")
            print(f"nf record is {row[6]}\n")
            commandlist.append(row[6])
            kubectllist.append(row[5])
            #newcommands=[commandlist.split(",")]
            print(f"dictlist is {commandlist[0]} and len is {len(commandlist)} and type is {type(commandlist)}")
            print(f"kubectl is {kubectllist[0]} and len is {len(kubectllist)} and type is {type(kubectllist)}")

     
    except Exception as e:
        print(f"{e}")

    finally:
        if (conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


    return commandlist


# list=readdbcommands()
# print(f"list is {list}")
# print(f"length of list is {len(list)}")
# for command in list:
#     print(command)