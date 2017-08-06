"""
接触tkinter……“坠好的学习就是写东西出来”……
一个双人游戏……
规则：
    红方与黑方
    红方先手
    轮流单击格子
    只能单击己方颜色的格子或是空白的格子
    若单击的是空白格子则该将格子涂上己方颜色
    若单击的是己方颜色的格子则：
        此格子变成空白
        并且相邻的格子中：
            空白涂上己方颜色
            对方颜色的格子和己方颜色的格子变成空白
    不能单击对方颜色的格子

    判胜：
        没想好……
        暂定一个颜色占满所有格子为胜吧
        判胜方法也没写到程序里面

    *记得修改矩阵的秩 n

    ---doudou
"""

from tkinter import Tk, Canvas, Frame, Button, ALL

# data
# n is the rank of the matrix
# ==========记得修改这个==========remember to modify n=========
n = 6
board = [[0 for i in range(n)] for i in range(n)]
colors = ['white', 'red', 'black']

# GUI

padding = 50

# containers

root = Tk()
root.title('Matrixdou')

frame_btns = Frame(root)
frame_btns.pack()

# canvas
canvas = Canvas(root, bg="white")
canvas.pack()

x_padding = y_padding = cell_width = cell_height = padding


def draw_matrix(matrix):
    # print('redraw')
    canvas.delete(ALL)

    width = 2 * x_padding + len(board) * cell_width
    height = 2 * y_padding + len(board) * cell_height
    canvas.config(width=width, height=height)

    for i in range(len(board)):
        for j in range(len(board[i])):
            index = board[i][j]
            color = colors[index]
            cellx = x_padding + i * cell_width
            celly = y_padding + j * cell_height
            item_tag = i.__repr__() + ',' + j.__repr__()
            canvas.create_rectangle(cellx, celly, cellx + cell_width, celly + cell_height,
                                           fill=color, outline="black", tags=item_tag)
    canvas.update()


# btns
def on_click_btn_clear():
    print('clear matrix')
    global board, player
    player = 1
    board = [[0 for i in range(n)] for i in range(n)]
    draw_matrix(board)


btn = Button(frame_btns, text='clear', command=on_click_btn_clear, height=3, width=8)
btn.pack()

# draw
draw_matrix(board)

# events
player = 1


def rev_cell(matrix, x, y, _player):
    if matrix[x][y] == 0:
        matrix[x][y] = _player
    else:
        matrix[x][y] = 0
    return matrix


def in_matrix(matrix, x, y):
    if x >= matrix.__len__() or y >= matrix[0].__len__() or x < 0 or y < 0:
        return False
    else:
        return True


def rev(matrix, x, y, p):
    if not in_matrix(matrix, x, y):
        return matrix, False

    if matrix[x][y] == 0:
        matrix[x][y] = p
    elif matrix[x][y] == p:
        matrix = rev_cell(matrix, x, y, p)
        if in_matrix(matrix, x + 1, y):
            matrix = rev_cell(matrix, x + 1, y, p)
        if in_matrix(matrix, x - 1, y):
            matrix = rev_cell(matrix, x - 1, y, p)
        if in_matrix(matrix, x, y + 1):
            matrix = rev_cell(matrix, x, y + 1, p)
        if in_matrix(matrix, x, y - 1):
            matrix = rev_cell(matrix, x, y - 1, p)
    else:
        return matrix, False

    return matrix, True


def on_click_item(x, y, tag_click):
    global board, player
    # rev data
    board, legal = rev(board, x, y, player)
    if legal:
        draw_matrix(board)
        player = player % 2 + 1
    else:
        print('operation illegal')


def on_click_canvas(event):
    x_index = int(event.x / 50) - 1
    y_index = int(event.y / 50) - 1
    tag_click = x_index.__repr__() + ',' + y_index.__repr__()
    # print(tag_click)
    on_click_item(x_index, y_index, tag_click)


canvas.bind('<Button-1>', on_click_canvas)

root.mainloop()
