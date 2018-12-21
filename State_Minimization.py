import pydotplus
from math import log2
O = 0
P = 0
S = 0
R = ''


def minimize(state_form):
    while True:
        # flag 用來辨認到底還有沒有相同能化簡的state
        flag = 1
        for mother in state_form:
            for kid in state_form[state_form.index(mother)+1:]:
                if (mother[1] == kid[1]) and (mother[2] == kid[2]):
                    flag = 0
                    replace = kid[0]
                    state_form.remove(kid)
                    # 一樣行為的state留一個，其他刪掉，也把所有state中出現被刪的next改成留下的那個
                    for state in state_form:
                        for next_state in state[1]:
                            if next_state == replace:
                                state[1][state[1].index(next_state)] = mother[0]
                            else:
                                pass
        if flag == 1:
            break
        else:
            pass
    return state_form


# 把讀入的 state description 做表格轉換
def form_transfer(set):
    form = []
    done_list = []
    for todo_group in set:
        present = todo_group[1]
        temp_list = []
        x_list = []
        next_state_list = []
        output_list = []
        if todo_group[1] in done_list:  # 過濾重複
            continue

        for i in set:
            if present == i[1]:
                temp_list.append(i)
            else:
                pass

        done_list.append(present)

        # 建立各筆state資料：
        # print(temp_list)
        # 建立 X_List 供後面辨識用，這邊為了辨識00 01 11 10 這類狀況，故先讓他們按順序排好
        for x in temp_list:
            x_list.append(int(x[0], 2))
        x_list.sort()

        # 根據x_list取對應值存放
        # print(x_list)
        for x in x_list:
            x_list[x_list.index(x)] = bin(x)[2:].zfill(len(bin(x_list[-1])[2:]))

        for x in x_list:
            for state in temp_list:
                if x == state[0]:
                    # next_state 整理
                    next_state_list.append(state[2])
                    # Output 整理
                    output_list.append(state[3])
                else:
                    pass
        form.append([present, next_state_list, output_list])

    # form 完成後來比對，並回傳
    return minimize(form)


# 開啟.kiss檔(需要再設定變動路徑)
file_name = input('請輸入要讀入之.kiss文件檔名(需在同資料夾)：')
f = open(file_name, 'r')
content = f.readlines()
new_content = []
f.close()

# 將讀進來的內容去除換行符號
for i in content:
    new_content.append(i.rstrip('\n'))

# 基礎參數取值與設定；
state_set = []
for i in new_content:
    command = i.split(" ")
    # print(i.split(' '))  # 輸出測試
    if command[0] == '.end_kiss':
        break
    elif command[0] == '.i':
        I = int(command[1])
    elif command[0] == '.o':
        O = int(command[1])
    elif command[0] == '.p':
        P = int(command[1])
    elif command[0] == '.s':
        S = int(command[1])
    elif command[0] == '.r':
        R = command[1]
    elif len(command) == 4:  # (state description)
        state_set.append(command)
# 轉成表格
minimized_form = form_transfer(state_set)
# 再轉成minimize_list
minimized_list = []
for state_group in minimized_form:
    temp = []
    x_digit = int(log2(len(state_group[1])))
    for i in range(x_digit+1):
        temp = [str(int(str(i), 2)), state_group[0], state_group[1][i], state_group[2][i]]
        minimized_list.append(temp)

# 計算Output後各屬性質數量
P = len(minimized_list)
S = len(minimized_form)

# 輸出output.kiss
# 建立新檔案(輸出文字檔)
new_file_path = '.\output_{0}'.format(file_name)
f = open(new_file_path, 'w')
f.write('.start_kiss\n')
f.write('.i {0}\n'.format(I))
f.write('.o {0}\n'.format(O))
f.write('.p {0}\n'.format(P))
f.write('.s {0}\n'.format(S))
f.write('.r {0}\n'.format(R))
for i in minimized_list:
    f.write('{0}\n'.format(' '.join(i)))
f.write('.end_kiss')
f.close()

# 繪圖
G_input = pydotplus.Dot(graph_type='digraph')
G_output = pydotplus.Dot(graph_type='digraph')
# G_in contribute
for i in state_set:
    io = '{0}/{1}'.format(i[0], i[3])
    edge = pydotplus.Edge('{0}'.format(i[1]), '{0}'.format(i[2]), label=io)
    G_input.add_edge(edge)

# G_out contribute
for i in minimized_list:
    io = '{0}/{1}'.format(i[0], i[3])
    edge = pydotplus.Edge('{0}'.format(i[1]), '{0}'.format(i[2]), label=io)
    G_output.add_edge(edge)

# 檔案輸出
G_input.write(file_name + '_input.dot')
G_input.write_png(file_name + '_input.png')
G_output.write(file_name + '_output.dot')
G_output.write_png(file_name + '_output.png')

# 輸出清單
print('輸出成功!!!!!')
print('共輸出 5 個檔案')
print('--------------')
print('1.{0}_input.dot'.format(file_name))
print('2.{0}_output.dot'.format(file_name))
print('3.{0}_input.png'.format(file_name))
print('4.{0}_output.png'.format(file_name))
print('5.output_{0}'.format(file_name))
print('---------------')
input('....按任意鍵繼續....')


