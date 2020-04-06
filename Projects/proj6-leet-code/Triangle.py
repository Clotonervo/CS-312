class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        previousRow = 0

        for row in range(len(triangle)):
            if row == 0:
                continue
            for index in range(len(triangle[row])):
                if index == 0:
                    triangle[row][index] = triangle[previousRow][index] + triangle[row][index]
                elif index == (len(triangle[row]) - 1):
                    triangle[row][index] = triangle[previousRow][index - 1] + triangle[row][index]
                else:
                    minValue = min(triangle[previousRow][index], triangle[previousRow][index - 1]) + triangle[row][index]
                    triangle[row][index] = minValue
            previousRow += 1

        return min(triangle[len(triangle) - 1])