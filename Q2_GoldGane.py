"""
【金币游戏】

任X堂要开发这样一个场景：存在一块二维方形地图（可由一个二维数组表示），地图的每个坐标看作一格，其中均放置了一枚金币；数组中的数字代表该格的高度；
马X奥只能上下左右四个方向前进，且每次只能跳到邻近格；马X奥可以从任何初始位置开始，但是只能往高处跳跃吃金币——即可以从高度1->2、1->3，
而不能1->1或2->1，求马里奥能吃到的最大金币数。
下面是一张示例地图：

1     2     3     4     5

16   17   18   19   6

15   24   25   20   7

14   23   22   21   8

13   12   11   10   9

对该图显然马X奥可以通过螺旋形路线吃到25枚金币。

算法输入：无，通过随机生成地图数据作为输入

算法输出：

1）按照示例地图的形式打印出随机生成的地图；

2）输出最大金币数和马X奥前进的路径，可自定义输出格式。
"""
import numpy as np


class TreeNode(object):

    def __init__(self, value=-2, x=-1, y=-1, left=None, right=None, up=None, down=None):
        self.value = value
        self.x = x
        self.y = y

        self.right = right
        self.left = left
        self.up = up
        self.down = down


class GoldGame(object):

    def __init__(self):

        self.start = None
        self.map = None
        self.axis_x = 5
        self.axis_y = 5
        self.random_seed = 0
        self.best_revenue = 0
        self.final_earnings = None

    def input_data(self, axis_x, axis_y, random_seed):
        """

        :param axis_x:
        :param axis_y:
        :param random_seed:
        :return:
        """
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.random_seed = random_seed

        self.map = np.random.randint(low=0, high=20, size=(self.axis_x, self.axis_y))
        self.final_earnings = np.zeros((self.axis_x, self.axis_y))

    def print_map(self):
        print(f'the map is shown below:')
        for row in self.map:
            for cell in row:
                print(str(cell).ljust(4), end='')
            print()

    def print_outcome(self):
        root = [[[] for j in range(self.axis_y)] for i in range(self.axis_x)]

        for m in range(self.axis_x):
            for n in range(self.axis_y):
                if self.final_earnings[m][n] == self.best_revenue:
                    print(f'The maximum profit can be obtained from point={(m, n)}, which is as follows')
                    root[m][n].append(TreeNode(value=self.best_revenue, x=m, y=n))
                    self.tree_explore(root[m][n][0], self.best_revenue)
                    self.generate_best_path(root[m][n][0])

    @staticmethod
    def move(x, y, action):
        if action == 1:
            x = x - 1
        if action == 2:
            x = x + 1
        if action == 3:
            y = y + 1
        if action == 4:
            y = y - 1
        return x, y

    def explore(self, x, y):

        gold_earning = 1  # start node gain 1

        for i in range(4):
            new_x, new_y = self.move(x, y, action=i + 1)

            # judge the move
            if (0 <= new_x < self.axis_x) and (0 <= new_y < self.axis_y) and (self.map[new_x][new_y] > self.map[x][y]):

                if self.explore(new_x, new_y) + 1 > gold_earning:
                    gold_earning = self.explore(new_x, new_y) + 1

        return gold_earning

    def calc_best_revenue(self):

        for x in range(self.axis_x):
            for y in range(self.axis_y):
                self.final_earnings[x][y] = self.explore(x, y)

                if self.final_earnings[x][y] > self.best_revenue:
                    self.best_revenue = self.final_earnings[x][y]

        return print(f'best revenue：{self.best_revenue}')

    def tree_explore(self, root, initial_revenue):
        """
        According to the return from each point, arrange the largest return in descending order,
        and find the corresponding income points in turn to obtain the path tree (multi-fork tree)
        :param root:
        :param initial_revenue:
        :return:
        """
        for action in range(4):
            new_x, new_y = self.move(root.x, root.y, action)

            if (0 <= new_x < self.axis_x) and (0 <= new_y < self.axis_y):
                if (self.final_earnings[new_x][new_y] == initial_revenue - 1) and (initial_revenue > 1) and (
                        self.map[new_x][new_y] > self.map[root.x][root.y]):
                    if action == 0:
                        temp_node = TreeNode(value=initial_revenue - 1, x=new_x, y=new_y)
                        root.left = temp_node
                        self.tree_explore(root.left, initial_revenue - 1)

                    elif action == 1:
                        temp_node = TreeNode(value=initial_revenue - 1, x=new_x, y=new_y)
                        root.right = temp_node
                        self.tree_explore(root.right, initial_revenue - 1)

                    elif action == 2:
                        temp_node = TreeNode(value=initial_revenue - 1, x=new_x, y=new_y)
                        root.up = temp_node
                        self.tree_explore(root.up, initial_revenue - 1)

                    elif action == 3:
                        temp_node = TreeNode(value=initial_revenue - 1, x=new_x, y=new_y)
                        root.down = temp_node
                        self.tree_explore(root.down, initial_revenue - 1)

    def generate_best_path(self, node):

        print(node.x, node.y)

        if (node.left is None) and (node.right is None) and (node.up is None) and (node.down is None):
            return None

        if node.left is not None:
            self.generate_best_path(node.left)

        if node.right is not None:
            self.generate_best_path(node.right)

        if node.up is not None:
            self.generate_best_path(node.up)

        if node.down is not None:
            self.generate_best_path(node.down)


gold_game = GoldGame()
gold_game.input_data(axis_x=4, axis_y=4, random_seed=0)
gold_game.print_map()
# calc best revenue
gold_game.calc_best_revenue()
# find the potential path
gold_game.print_outcome()