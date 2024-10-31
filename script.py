from typing import List
import logging

class Solution:
    def countGoodRectangles(self, rectangles: List[List[int]]) -> int:
        # defining rectangle with max sides
        # counting
        max_len = int(min(rectangles[0]))
        for rectange in rectangles:
            if int(min(rectange)) > max_len:
                max_len = min(rectange)
        
        result = 0
        for rectangle in rectangles:
            if int(min(rectangle)) >= max_len:
                result += 1

        return result

rectangles = [[2,3],[3,7],[4,3],[3,7]]
solution = Solution()
print(solution.countGoodRectangles(rectangles))