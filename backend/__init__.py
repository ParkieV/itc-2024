class Solution:
    def generate(self, numRows: int):
        result = []
        if numRows == 0:
            result = []
        elif numRows == 1:
            result = [[1]]
        elif numRows == 2:
            result = [[1], [1, 1]]
        else:
            result = [[1], [1, 1]]
            for i in range(2, numRows):
                result.append([1])
                for j in range(1, len(result[i - 1])):
                    result[i].append(result[i-1][j] + result[i-1][j - 1])
                result[i].append(1)
        return result


print(Solution().generate(5))
