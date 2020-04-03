class Solution:
    def tribonacci(self, n: int) -> int:
        sol = [0] * 38
        sol[1] = 1
        sol[2] = 1
        for i in range(35):
            sol[i + 3] = sol[i] + sol[i + 1] + sol[i + 2]

        # print(sol)
        # print(n)
        return sol[n]
        
