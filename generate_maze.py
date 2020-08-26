# -*- coding: utf-8 -*-

"""迷路生成
"""

import sys
import numpy as np
import matplotlib.pyplot as plt


class Maze:
    WALL, PATH = 0, 1

    def __init__(self, width, height):
        """
        迷路のサイズを指定して、行列を経路で初期化
        :param width: 横
        :param height: 縦
        """
        # 指定されたサイズの確認
        if width < 3 or height < 3:
            print('3 x 3 以上のサイズを指定してください.')
            sys.exit(1)
        if width % 2 == 0 or height % 2 == 0:
            print('サイズは奇数を指定してください.')
            sys.exit(1)
        # 行列のサイズなので、整数値にキャストしている
        self.__width = int(width)
        self.__height = int(height)
        # マップ全域を経路として初期化
        self.__map = np.ones((self.__height, self.__width), dtype=np.int8)

    def save(self, filename):
        """
        迷路を画像で保存
        :return: なし
        """
        fig = plt.figure(frameon=False)
        fig.set_size_inches(self.__width * 10, self.__height * 10)
        ax = plt.Axes(fig, [0, 0, 1, 1])
        ax.set_axis_off()
        fig.add_axes(ax)
        img = ax.imshow(self.__map, interpolation='nearest')
        img.set_cmap('tab20')
        fig.savefig(filename, dpi=1)
        print('{0}で保存しました.'.format(filename))

    def generate(self, seed_value=None):
        """
        迷路を生成
        :param seed_value: シード値 (オプション)
        :return: なし
        """
        if seed_value is not None:
            np.random.seed(seed_value)
        self.__divide(Area(0, 0, self.__width-1, self.__height-1))

    def __divide(self, area):
        """
        引数の領域を分割
        :param area: 分割対象の領域情報
        :return: なし
        """
        # 一辺でも長さが1ならば終了
        if area.width <= 1 or area.height <= 1:
            return
        # 分割する方向を決定 (長辺の方向で分割)
        # 例. 縦辺の方が横辺より長い場合は水平方向で分割
        is_horizontal = np.random.choice([False, True]) if area.width == area.height else area.width > area.height
        # 以下、分割処理
        if is_horizontal:
            # 水平方向に分割
            x = self.__divide_horizontally(area)
            # 再帰呼出
            self.__divide(Area(area.min_x, area.min_y, x-1, area.max_y))
            self.__divide(Area(x+1, area.min_y, area.max_x, area.max_y))
        else:
            # 垂直方向に分割
            y = self.__divide_vertically(area)
            # 再帰呼出
            self.__divide(Area(area.min_x, area.min_y, area.max_x, y-1))
            self.__divide(Area(area.min_x, y+1, area.max_x, area.max_y))

    def __divide_horizontally(self, area):
        """
        引数の領域を水平方向に分割
        :param area: 分割対象の領域情報
        :return: 分割するx位置
        """
        # 穴を空ける位置を決定
        x = area.min_x + 1
        if area.width >= 2:
            x += np.random.randint(area.width / 2) * 2

        # 壁の位置を決定
        y = area.min_y
        if area.height == 3:
            y += np.random.randint(2) * 2
        elif area.height > 3:
            y += np.random.randint(area.height / 2) * 2

        self.__map[area.min_y:area.max_y+1, x] = Maze.WALL
        self.__map[y, x] = Maze.PATH
        return x

    def __divide_vertically(self, area):
        """
        引数の領域を垂直方向に分割
        :param area: 分割対象の領域情報
        :return: 分割するy位置
        """
        # 壁の位置を決定
        x = area.min_x
        if area.width == 3:
            x += np.random.randint(2) * 2
        elif area.width > 3:
            x += np.random.randint(area.width / 2) * 2

        # 穴を空ける位置を決定
        y = area.min_y + 1
        if area.height >= 2:
            y += np.random.randint(area.height / 2) * 2

        self.__map[y, area.min_x:area.max_x+1] = Maze.WALL
        self.__map[y, x] = Maze.PATH
        return y


class Area:
    def __init__(self, min_x, min_y, max_x, max_y):
        """
        領域の定義
        :param min_x: 始点x
        :param min_y: 始点y
        :param max_x: 終点x
        :param max_y: 終点y
        """
        self.__min_x = min_x
        self.__min_y = min_y
        self.__max_x = max_x
        self.__max_y = max_y
        # サイズなので+1している
        self.__width = max_x - min_x + 1
        self.__height = max_y - min_y + 1

    @property
    def min_x(self):
        return self.__min_x

    @property
    def min_y(self):
        return self.__min_y

    @property
    def max_x(self):
        return self.__max_x

    @property
    def max_y(self):
        return self.__max_y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python {0} width height'.format(sys.argv[0]))
        sys.exit(1)

    maze = Maze(int(sys.argv[1]), int(sys.argv[2]))
    # maze.generate(65532)  # シード値設定可能
    maze.save('./maze_img/{0}x{1}.png'.format(sys.argv[1], sys.argv[2]))
