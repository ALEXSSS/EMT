import sqlite3

con = sqlite3.connect("firstDb.db")
cur = con.cursor()
if __name__ == "__main__":
    cursor = con.execute(
        "SELECT distinct CliCode from "
        "info_cli_otgr_201503 as a")
    i = 0;
    # listOfCliCode=[a[0] for a in cursor]
    cursorRgdCode = con.execute(
        "SELECT RgdCode from " +
        "info_rgd_desc")

    RgdCode = {}
    i = 0;
    for rgd in cursorRgdCode:
        RgdCode[i] = rgd;
        i += 1;
   # print(RgdCode)
    vectorOfCustomers = {a[0]: [0 for k in range(len(RgdCode))] for a in cursor}
    print(vectorOfCustomers)

    for group in RgdCode.keys():
        cursor1 = con.execute(
            "SELECT CliCode, RgdQuant from "
            "info_cli_otgr_201503 as a where RgdCode=\"" + group + "\" ")
        listOfCliCode = [(a[0], str(round(float(a[1])))) for a in cursor1]
        list=[a[1] for a in listOfCliCode]
        for cliCode in listOfCliCode:
          try:
            vectorOfCustomers.get(cliCode[0])[RgdCode.get(group)]=str(
                int(vectorOfCustomers.get(cliCode[0])[RgdCode.get(group)]) + int(cliCode[1]))
          except Exception:
            print("Fallen")
            print(vectorOfCustomers.get(cliCode[0]))
            print(cliCode)
            print("====================================================================")
    print(vectorOfCustomers.get("1"))
