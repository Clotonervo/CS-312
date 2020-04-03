class Solution:
    def gardenNoAdj(self, N: int, paths: List[List[int]]) -> List[int]:
        colors = [-1] * N
        adj_list = [[] for i in range(N)]
        for path in paths:
            if (path[1] - 1) not in adj_list[path[0] - 1]:
                adj_list[path[0] - 1].append(path[1] - 1)
            if (path[0] - 1) not in adj_list[path[1] - 1]:
                adj_list[path[1] - 1].append(path[0] - 1)
        print(adj_list)

        for i in range(N):
            available_colors = [1,2,3,4]
            for j in adj_list[i]:
                if colors[j] in available_colors:
                    available_colors.remove(colors[j])
            colors[i] = available_colors.pop()
        return colors
