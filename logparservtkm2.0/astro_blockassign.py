
import sys
# normal iteration over 128 blocks
for x in range(0,4,1):
    for y in range(0,4,1):
        for z in range(0,8,1):
            id = x*32+y*8+z
            print(z,y,x,"id",id)

# dividing to 2*2*4 = 16 groups
# mapping the x y z into the group id
g_size_x=2
g_num_x =2
g_size_y=2
g_num_y =2
# z dim is as 3 2 3
#g_size_z=2 
g_num_z =3

group_list=[]
for i in range(0,g_num_x*g_num_y*g_num_z,1):
    group_list.append([])

for x in range(0,4,1):
    for y in range(0,4,1):
        for z in range(0,8,1):
            id = x*32+y*8+z
            # size of group in each dimention
            g_id_x=int(x/g_size_x)
            g_id_y=int(y/g_size_y)
            g_id_z = 0
            temp = int(z%8) 
            if temp>=0 and temp<=2:
                g_id_z=0
            elif temp>=3 and temp<=4:
                g_id_z=1
            else:
                g_id_z=2
            # number of element in each group
            groupid = g_id_x*g_num_y*g_num_z+g_id_y*g_num_z+g_id_z

            id = x*32+y*8+z
            print(z,y,x,"id",id, "group id", groupid)

            group_list[groupid].append(id)


rank=0
for g in group_list:
    print("rank", rank, end=": ")
    for v in g:
        print(v,end=" ")
    print("")
    rank+=1