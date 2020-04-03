
class Solution:
    def nth_index(self, iterable, value, n):
        matches = (idx for idx, val in enumerate(iterable) if val == value)
        return next(islice(matches, n-1, n), None)

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # nums.sort()
        sorted_nums = sorted(nums)
        print(sorted_nums)
        i = 0;
        j = 0;
        for number1 in sorted_nums:
            j = 0;
            if number1 > target and target > 0:
                return []

            for number2 in sorted_nums:
                if i != j:
                    if (number1 + number2) == target:
                        i_index = nums.index(number1)
                        j_index = nums.index(number2)
                        print(i_index, " ", j_index)
                        if i_index == j_index:
                            j_index = self.nth_index(nums, number2, 2)

                        return [i_index, j_index]
                    elif (number1 + number2) > target:
                        break
                j += 1
            i += 1;
