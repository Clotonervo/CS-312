class Solution:
    def maxArea(self, height: List[int]) -> int:
        currRightIndex = len(height) - 1
        currLeftIndex = 0
        maxArea = 0

        while(currLeftIndex < currRightIndex):
            currentHeight = min(height[currRightIndex], height[currLeftIndex])
            currentWidth = currRightIndex - currLeftIndex
            tempArea = currentHeight * currentWidth
            if(tempArea > maxArea):
                maxArea = tempArea

            if(height[currRightIndex] > height[currLeftIndex]):
                currLeftIndex += 1
            else:
                currRightIndex -= 1

        return maxArea
        
