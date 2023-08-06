def parse_res(lines):
    data = {}
    inblock_field = []
    outblock_field = []

    parse_mode = 0        # 0: none, 1: inblock, 2: outblock
    req_mode = 0          # 0: TR, 1: Real

    for line in lines:
        strip_line = line.strip()

        if strip_line.startswith((".Func", ".Feed")):
            # TR 목록/Real 목록
            if strip_line.startswith(".Func"):
                req_mode = 0
            else:
                req_mode = 1

            tokens = strip_line.split(',')
            data['name'] = tokens[2].strip()
            continue

        if "InBlock" in strip_line:
            parse_mode = 1
            continue

        if "OutBlock" in strip_line:
            parse_mode = 2
            continue

        if "END_DATA_MAP" in strip_line:
            parse_mode = 0
            continue

        if parse_mode == 1 and strip_line != 'begin' and strip_line != 'end':
            fields = strip_line.split(',')
            field = fields[1].strip()
            inblock_field.append(field)

        if parse_mode == 2 and strip_line != 'begin' and strip_line != 'end':
            fields = strip_line.split(',')
            field = fields[1].strip()
            outblock_field.append(field)


    if req_mode == 0:
        data['inblock'] = data['name'] + "InBlock"
        data['outblock'] = data['name'] + "OutBlock"
    else:
        data['inblock'] = "InBlock"
        data['outblock'] = "OutBlock"

    data['inblock_field'] = inblock_field
    data['outblock_field'] = outblock_field
    return data


if __name__ == "__main__":
    # TR(t8340)
    #f = open("c:/eBEST/xingAPI/Res/t8430.res", encoding="euc-kr")
    #lines = f.readlines()
    #f.close()

    # Real
    f = open("c:/eBEST/xingAPI/Res/NWS.res", encoding="euc-kr")
    lines = f.readlines()
    f.close()

    import pprint
    data = parse_res(lines)
    pprint.pprint(data)


