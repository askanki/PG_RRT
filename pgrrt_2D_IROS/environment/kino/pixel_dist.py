def dist(pixel1, pixel2):
    if((pixel1[0] - pixel2[0])**2 + (pixel1[0] - pixel2[0])**2)**0.5 > 10:
        return True
    return False

file = open("debug.txt", "r")
line = file.readline()
pixel_map = {}
count = 0
while(line):
    line = line.split(" ")

    if (line[0] == "[event_track_features]" and line[1] == "Feature"):
        # print(line)
        # break
        line[4] = line[4][1:]
        if int(line[4]) not in pixel_map:
            pixel_map[int(line[4])] = []
            count +=1
        # if count>2:
        #     break
        pixel_map[int(line[4])].append((int(line[5+4][2:-1]), int(line[6+4][:-1])))
        if(len(pixel_map[int(line[4])]) > 1):
            if dist(pixel_map[int(line[4])][-1], pixel_map[int(line[4])][-2]):
                print(int(line[4]), pixel_map[int(line[4])][-1], pixel_map[int(line[4])][-2])
    line = file.readline()

print(count)
# print(pixel_map)