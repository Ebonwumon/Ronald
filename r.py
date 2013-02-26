infile = open("edmonton-roads-digraph.txt", "r")
for line in infile:
    line = line.rstrip()
    fields = line.split(",")

    type = fields.pop(0)

    if type == "E":
        # print(fields)

        (start, stop, name) = fields

        name = name.strip('"')

        print("{}->{}:{}".format(int(start), int(stop), name))

    #print("<" + line + ">")
