from django.core.management.base import BaseCommand
from django.utils.text import slugify

from problems.models import Problem, Topic, Tag


"""
═══════════════════════════════════════════════════════════════
50+ CODING PROBLEMS FOR YOUR PLATFORM
Carefully curated from easy to hard with complete details
═══════════════════════════════════════════════════════════════
"""

PROBLEMS = [
    # ═══════════════════════════════════════════════════════════
    # EASY PROBLEMS (20 problems)
    # ═══════════════════════════════════════════════════════════
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "EASY",
        "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.""",
        "examples": """Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]""",
        "constraints": """• 2 <= nums.length <= 10^4
• -10^9 <= nums[i] <= 10^9
• -10^9 <= target <= 10^9
• Only one valid answer exists.""",
        "topics": ["Array", "Hash Table"],
        "tags": ["Arrays", "Hashing"],
        "points": 5,
        "acceptance_rate": 48.5,
    },
    {
        "title": "Palindrome Number",
        "slug": "palindrome-number",
        "difficulty": "EASY",
        "description": """Given an integer x, return true if x is a palindrome, and false otherwise.

An integer is a palindrome when it reads the same backward as forward.""",
        "examples": """Example 1:
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

Example 2:
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

Example 3:
Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.""",
        "constraints": """• -2^31 <= x <= 2^31 - 1""",
        "topics": ["Math"],
        "tags": ["Math", "Numbers"],
        "points": 5,
        "acceptance_rate": 52.3,
    },
    {
        "title": "Roman to Integer",
        "slug": "roman-to-integer",
        "difficulty": "EASY",
        "description": """Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000

Given a roman numeral, convert it to an integer.""",
        "examples": """Example 1:
Input: s = "III"
Output: 3
Explanation: III = 3.

Example 2:
Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.

Example 3:
Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.""",
        "constraints": """• 1 <= s.length <= 15
• s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M')
• It is guaranteed that s is a valid roman numeral in the range [1, 3999]""",
        "topics": ["Hash Table", "Math", "String"],
        "tags": ["Strings", "Math"],
        "points": 5,
        "acceptance_rate": 58.7,
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "difficulty": "EASY",
        "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.""",
        "examples": """Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false""",
        "constraints": """• 1 <= s.length <= 10^4
• s consists of parentheses only '()[]{}'""",
        "topics": ["String", "Stack"],
        "tags": ["Stack", "Strings"],
        "points": 5,
        "acceptance_rate": 40.2,
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "difficulty": "EASY",
        "description": """You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.""",
        "examples": """Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:
Input: list1 = [], list2 = []
Output: []

Example 3:
Input: list1 = [], list2 = [0]
Output: [0]""",
        "constraints": """• The number of nodes in both lists is in the range [0, 50]
• -100 <= Node.val <= 100
• Both list1 and list2 are sorted in non-decreasing order""",
        "topics": ["Linked List", "Recursion"],
        "tags": ["Linked List", "Recursion"],
        "points": 5,
        "acceptance_rate": 61.8,
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "difficulty": "EASY",
        "description": """You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.""",
        "examples": """Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.

Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.""",
        "constraints": """• 1 <= prices.length <= 10^5
• 0 <= prices[i] <= 10^4""",
        "topics": ["Array", "Dynamic Programming"],
        "tags": ["Arrays", "Dynamic Programming"],
        "points": 5,
        "acceptance_rate": 54.3,
    },
    {
        "title": "Valid Anagram",
        "slug": "valid-anagram",
        "difficulty": "EASY",
        "description": """Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.""",
        "examples": """Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false""",
        "constraints": """• 1 <= s.length, t.length <= 5 * 10^4
• s and t consist of lowercase English letters""",
        "topics": ["Hash Table", "String", "Sorting"],
        "tags": ["Hashing", "Strings", "Sorting"],
        "points": 5,
        "acceptance_rate": 62.1,
    },
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "difficulty": "EASY",
        "description": """Given the head of a singly linked list, reverse the list, and return the reversed list.""",
        "examples": """Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []""",
        "constraints": """• The number of nodes in the list is the range [0, 5000]
• -5000 <= Node.val <= 5000""",
        "topics": ["Linked List", "Recursion"],
        "tags": ["Linked List", "Recursion"],
        "points": 5,
        "acceptance_rate": 71.2,
    },
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "difficulty": "EASY",
        "description": """Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.""",
        "examples": """Example 1:
Input: nums = [1,2,3,1]
Output: true

Example 2:
Input: nums = [1,2,3,4]
Output: false

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true""",
        "constraints": """• 1 <= nums.length <= 10^5
• -10^9 <= nums[i] <= 10^9""",
        "topics": ["Array", "Hash Table", "Sorting"],
        "tags": ["Arrays", "Hashing"],
        "points": 5,
        "acceptance_rate": 60.5,
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "difficulty": "EASY",
        "description": """Given an integer array nums, find the subarray with the largest sum, and return its sum.""",
        "examples": """Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.""",
        "constraints": """• 1 <= nums.length <= 10^5
• -10^4 <= nums[i] <= 10^4""",
        "topics": ["Array", "Dynamic Programming", "Divide and Conquer"],
        "tags": ["Arrays", "Dynamic Programming"],
        "points": 5,
        "acceptance_rate": 49.7,
    },
    {
        "title": "Climbing Stairs",
        "slug": "climbing-stairs",
        "difficulty": "EASY",
        "description": """You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?""",
        "examples": """Example 1:
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step""",
        "constraints": """• 1 <= n <= 45""",
        "topics": ["Math", "Dynamic Programming", "Memoization"],
        "tags": ["Dynamic Programming", "Math"],
        "points": 5,
        "acceptance_rate": 51.3,
    },
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "difficulty": "EASY",
        "description": """Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.""",
        "examples": """Example 1:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1""",
        "constraints": """• 1 <= nums.length <= 10^4
• -10^4 < nums[i], target < 10^4
• All the integers in nums are unique
• nums is sorted in ascending order""",
        "topics": ["Array", "Binary Search"],
        "tags": ["Binary Search", "Arrays"],
        "points": 5,
        "acceptance_rate": 55.8,
    },
    {
        "title": "Linked List Cycle",
        "slug": "linked-list-cycle",
        "difficulty": "EASY",
        "description": """Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer.""",
        "examples": """Example 1:
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

Example 2:
Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.

Example 3:
Input: head = [1], pos = -1
Output: false
Explanation: There is no cycle in the linked list.""",
        "constraints": """• The number of the nodes in the list is in the range [0, 10^4]
• -10^5 <= Node.val <= 10^5
• pos is -1 or a valid index in the linked-list""",
        "topics": ["Hash Table", "Linked List", "Two Pointers"],
        "tags": ["Linked List", "Two Pointers"],
        "points": 5,
        "acceptance_rate": 47.2,
    },
    {
        "title": "Missing Number",
        "slug": "missing-number",
        "difficulty": "EASY",
        "description": """Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.""",
        "examples": """Example 1:
Input: nums = [3,0,1]
Output: 2
Explanation: n = 3 since there are 3 numbers, so all numbers are in the range [0,3]. 2 is the missing number in the range since it does not appear in nums.

Example 2:
Input: nums = [0,1]
Output: 2
Explanation: n = 2 since there are 2 numbers, so all numbers are in the range [0,2]. 2 is the missing number in the range since it does not appear in nums.

Example 3:
Input: nums = [9,6,4,2,3,5,7,0,1]
Output: 8
Explanation: n = 9 since there are 9 numbers, so all numbers are in the range [0,9]. 8 is the missing number in the range since it does not appear in nums.""",
        "constraints": """• n == nums.length
• 1 <= n <= 10^4
• 0 <= nums[i] <= n
• All the numbers of nums are unique""",
        "topics": ["Array", "Hash Table", "Math", "Binary Search", "Bit Manipulation", "Sorting"],
        "tags": ["Arrays", "Math", "Bit Manipulation"],
        "points": 5,
        "acceptance_rate": 60.3,
    },
    {
        "title": "Move Zeroes",
        "slug": "move-zeroes",
        "difficulty": "EASY",
        "description": """Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.""",
        "examples": """Example 1:
Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

Example 2:
Input: nums = [0]
Output: [0]""",
        "constraints": """• 1 <= nums.length <= 10^4
• -2^31 <= nums[i] <= 2^31 - 1""",
        "topics": ["Array", "Two Pointers"],
        "tags": ["Arrays", "Two Pointers"],
        "points": 5,
        "acceptance_rate": 60.9,
    },
    {
        "title": "Intersection of Two Arrays II",
        "slug": "intersection-of-two-arrays-ii",
        "difficulty": "EASY",
        "description": """Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must appear as many times as it shows in both arrays and you may return the result in any order.""",
        "examples": """Example 1:
Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2,2]

Example 2:
Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [4,9]
Explanation: [9,4] is also accepted.""",
        "constraints": """• 1 <= nums1.length, nums2.length <= 1000
• 0 <= nums1[i], nums2[i] <= 1000""",
        "topics": ["Array", "Hash Table", "Two Pointers", "Binary Search", "Sorting"],
        "tags": ["Arrays", "Hashing", "Two Pointers"],
        "points": 5,
        "acceptance_rate": 54.6,
    },
    {
        "title": "First Bad Version",
        "slug": "first-bad-version",
        "difficulty": "EASY",
        "description": """You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

Suppose you have n versions [1, 2, ..., n] and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API bool isBadVersion(version) which returns whether version is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.""",
        "examples": """Example 1:
Input: n = 5, bad = 4
Output: 4
Explanation:
call isBadVersion(3) -> false
call isBadVersion(5) -> true
call isBadVersion(4) -> true
Then 4 is the first bad version.

Example 2:
Input: n = 1, bad = 1
Output: 1""",
        "constraints": """• 1 <= bad <= n <= 2^31 - 1""",
        "topics": ["Binary Search", "Interactive"],
        "tags": ["Binary Search"],
        "points": 5,
        "acceptance_rate": 41.2,
    },
    {
        "title": "Fizz Buzz",
        "slug": "fizz-buzz",
        "difficulty": "EASY",
        "description": """Given an integer n, return a string array answer (1-indexed) where:
• answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
• answer[i] == "Fizz" if i is divisible by 3.
• answer[i] == "Buzz" if i is divisible by 5.
• answer[i] == i (as a string) if none of the above conditions are true.""",
        "examples": """Example 1:
Input: n = 3
Output: ["1","2","Fizz"]

Example 2:
Input: n = 5
Output: ["1","2","Fizz","4","Buzz"]

Example 3:
Input: n = 15
Output: ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]""",
        "constraints": """• 1 <= n <= 10^4""",
        "topics": ["Math", "String", "Simulation"],
        "tags": ["Math", "Strings"],
        "points": 5,
        "acceptance_rate": 69.8,
    },
    {
        "title": "Power of Three",
        "slug": "power-of-three",
        "difficulty": "EASY",
        "description": """Given an integer n, return true if it is a power of three. Otherwise, return false.

An integer n is a power of three, if there exists an integer x such that n == 3^x.""",
        "examples": """Example 1:
Input: n = 27
Output: true
Explanation: 27 = 3^3

Example 2:
Input: n = 0
Output: false
Explanation: There is no x where 3^x = 0.

Example 3:
Input: n = -1
Output: false
Explanation: There is no x where 3^x = (-1).""",
        "constraints": """• -2^31 <= n <= 2^31 - 1""",
        "topics": ["Math", "Recursion"],
        "tags": ["Math", "Recursion"],
        "points": 5,
        "acceptance_rate": 45.3,
    },
    {
        "title": "Majority Element",
        "slug": "majority-element",
        "difficulty": "EASY",
        "description": """Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.""",
        "examples": """Example 1:
Input: nums = [3,2,3]
Output: 3

Example 2:
Input: nums = [2,2,1,1,1,2,2]
Output: 2""",
        "constraints": """• n == nums.length
• 1 <= n <= 5 * 10^4
• -10^9 <= nums[i] <= 10^9""",
        "topics": ["Array", "Hash Table", "Divide and Conquer", "Sorting", "Counting"],
        "tags": ["Arrays", "Hashing", "Sorting"],
        "points": 5,
        "acceptance_rate": 63.7,
    },

    # ═══════════════════════════════════════════════════════════
    # MEDIUM PROBLEMS (20 problems)
    # ═══════════════════════════════════════════════════════════
    {
        "title": "Add Two Numbers",
        "slug": "add-two-numbers",
        "difficulty": "MEDIUM",
        "description": """You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.""",
        "examples": """Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]""",
        "constraints": """• The number of nodes in each linked list is in the range [1, 100]
• 0 <= Node.val <= 9
• It is guaranteed that the list represents a number that does not have leading zeros""",
        "topics": ["Linked List", "Math", "Recursion"],
        "tags": ["Linked List", "Math"],
        "points": 10,
        "acceptance_rate": 40.8,
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "difficulty": "MEDIUM",
        "description": """Given a string s, find the length of the longest substring without repeating characters.""",
        "examples": """Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.""",
        "constraints": """• 0 <= s.length <= 5 * 10^4
• s consists of English letters, digits, symbols and spaces""",
        "topics": ["Hash Table", "String", "Sliding Window"],
        "tags": ["Sliding Window", "Hashing", "Strings"],
        "points": 10,
        "acceptance_rate": 33.7,
    },
    {
        "title": "3Sum",
        "slug": "3sum",
        "difficulty": "MEDIUM",
        "description": """Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.""",
        "examples": """Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.""",
        "constraints": """• 3 <= nums.length <= 3000
• -10^5 <= nums[i] <= 10^5""",
        "topics": ["Array", "Two Pointers", "Sorting"],
        "tags": ["Arrays", "Two Pointers", "Sorting"],
        "points": 10,
        "acceptance_rate": 31.2,
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "difficulty": "MEDIUM",
        "description": """You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.""",
        "examples": """Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

Example 2:
Input: height = [1,1]
Output: 1""",
        "constraints": """• n == height.length
• 2 <= n <= 10^5
• 0 <= height[i] <= 10^4""",
        "topics": ["Array", "Two Pointers", "Greedy"],
        "tags": ["Arrays", "Two Pointers", "Greedy"],
        "points": 10,
        "acceptance_rate": 53.4,
    },
    {
        "title": "Letter Combinations of a Phone Number",
        "slug": "letter-combinations-of-a-phone-number",
        "difficulty": "MEDIUM",
        "description": """Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

2: abc, 3: def, 4: ghi, 5: jkl, 6: mno, 7: pqrs, 8: tuv, 9: wxyz""",
        "examples": """Example 1:
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:
Input: digits = ""
Output: []

Example 3:
Input: digits = "2"
Output: ["a","b","c"]""",
        "constraints": """• 0 <= digits.length <= 4
• digits[i] is a digit in the range ['2', '9']""",
        "topics": ["Hash Table", "String", "Backtracking"],
        "tags": ["Backtracking", "Strings", "Recursion"],
        "points": 10,
        "acceptance_rate": 55.8,
    },
    {
        "title": "Generate Parentheses",
        "slug": "generate-parentheses",
        "difficulty": "MEDIUM",
        "description": """Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.""",
        "examples": """Example 1:
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:
Input: n = 1
Output: ["()"]""",
        "constraints": """• 1 <= n <= 8""",
        "topics": ["String", "Dynamic Programming", "Backtracking"],
        "tags": ["Backtracking", "Strings", "Dynamic Programming"],
        "points": 10,
        "acceptance_rate": 71.3,
    },
    {
        "title": "Permutations",
        "slug": "permutations",
        "difficulty": "MEDIUM",
        "description": """Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.""",
        "examples": """Example 1:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Example 2:
Input: nums = [0,1]
Output: [[0,1],[1,0]]

Example 3:
Input: nums = [1]
Output: [[1]]""",
        "constraints": """• 1 <= nums.length <= 6
• -10 <= nums[i] <= 10
• All the integers of nums are unique""",
        "topics": ["Array", "Backtracking"],
        "tags": ["Backtracking", "Arrays", "Recursion"],
        "points": 10,
        "acceptance_rate": 75.2,
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "difficulty": "MEDIUM",
        "description": """Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.""",
        "examples": """Example 1:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
Input: strs = [""]
Output: [[""]]

Example 3:
Input: strs = ["a"]
Output: [["a"]]""",
        "constraints": """• 1 <= strs.length <= 10^4
• 0 <= strs[i].length <= 100
• strs[i] consists of lowercase English letters""",
        "topics": ["Array", "Hash Table", "String", "Sorting"],
        "tags": ["Hashing", "Strings", "Sorting"],
        "points": 10,
        "acceptance_rate": 66.4,
    },
    {
        "title": "Rotate Image",
        "slug": "rotate-image",
        "difficulty": "MEDIUM",
        "description": """You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.""",
        "examples": """Example 1:
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[7,4,1],[8,5,2],[9,6,3]]

Example 2:
Input: matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]""",
        "constraints": """• n == matrix.length == matrix[i].length
• 1 <= n <= 20
• -1000 <= matrix[i][j] <= 1000""",
        "topics": ["Array", "Math", "Matrix"],
        "tags": ["Arrays", "Matrix", "Math"],
        "points": 10,
        "acceptance_rate": 68.9,
    },
    {
        "title": "Spiral Matrix",
        "slug": "spiral-matrix",
        "difficulty": "MEDIUM",
        "description": """Given an m x n matrix, return all elements of the matrix in spiral order.""",
        "examples": """Example 1:
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]

Example 2:
Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]""",
        "constraints": """• m == matrix.length
• n == matrix[i].length
• 1 <= m, n <= 10
• -100 <= matrix[i][j] <= 100""",
        "topics": ["Array", "Matrix", "Simulation"],
        "tags": ["Arrays", "Matrix", "Simulation"],
        "points": 10,
        "acceptance_rate": 44.3,
    },
    {
        "title": "Jump Game",
        "slug": "jump-game",
        "difficulty": "MEDIUM",
        "description": """You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.""",
        "examples": """Example 1:
Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
Input: nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.""",
        "constraints": """• 1 <= nums.length <= 10^4
• 0 <= nums[i] <= 10^5""",
        "topics": ["Array", "Dynamic Programming", "Greedy"],
        "tags": ["Arrays", "Dynamic Programming", "Greedy"],
        "points": 10,
        "acceptance_rate": 38.5,
    },
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "difficulty": "MEDIUM",
        "description": """Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.""",
        "examples": """Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.""",
        "constraints": """• 1 <= intervals.length <= 10^4
• intervals[i].length == 2
• 0 <= starti <= endi <= 10^4""",
        "topics": ["Array", "Sorting"],
        "tags": ["Arrays", "Sorting", "Intervals"],
        "points": 10,
        "acceptance_rate": 46.2,
    },
    {
        "title": "Unique Paths",
        "slug": "unique-paths",
        "difficulty": "MEDIUM",
        "description": """There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.""",
        "examples": """Example 1:
Input: m = 3, n = 7
Output: 28

Example 2:
Input: m = 3, n = 2
Output: 3
Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down""",
        "constraints": """• 1 <= m, n <= 100""",
        "topics": ["Math", "Dynamic Programming", "Combinatorics"],
        "tags": ["Dynamic Programming", "Math", "Grid"],
        "points": 10,
        "acceptance_rate": 62.7,
    },
    {
        "title": "Minimum Path Sum",
        "slug": "minimum-path-sum",
        "difficulty": "MEDIUM",
        "description": """Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.""",
        "examples": """Example 1:
Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
Explanation: Because the path 1 → 3 → 1 → 1 → 1 minimizes the sum.

Example 2:
Input: grid = [[1,2,3],[4,5,6]]
Output: 12""",
        "constraints": """• m == grid.length
• n == grid[i].length
• 1 <= m, n <= 200
• 0 <= grid[i][j] <= 200""",
        "topics": ["Array", "Dynamic Programming", "Matrix"],
        "tags": ["Dynamic Programming", "Matrix", "Grid"],
        "points": 10,
        "acceptance_rate": 61.3,
    },
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "difficulty": "MEDIUM",
        "description": """There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.""",
        "examples": """Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:
Input: nums = [1], target = 0
Output: -1""",
        "constraints": """• 1 <= nums.length <= 5000
• -10^4 <= nums[i] <= 10^4
• All values of nums are unique
• nums is an ascending array that is possibly rotated
• -10^4 <= target <= 10^4""",
        "topics": ["Array", "Binary Search"],
        "tags": ["Binary Search", "Arrays"],
        "points": 10,
        "acceptance_rate": 38.9,
    },
    {
        "title": "Find First and Last Position of Element in Sorted Array",
        "slug": "find-first-and-last-position-of-element-in-sorted-array",
        "difficulty": "MEDIUM",
        "description": """Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.""",
        "examples": """Example 1:
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Example 2:
Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Example 3:
Input: nums = [], target = 0
Output: [-1,-1]""",
        "constraints": """• 0 <= nums.length <= 10^5
• -10^9 <= nums[i] <= 10^9
• nums is a non-decreasing array
• -10^9 <= target <= 10^9""",
        "topics": ["Array", "Binary Search"],
        "tags": ["Binary Search", "Arrays"],
        "points": 10,
        "acceptance_rate": 41.8,
    },
    {
        "title": "Combination Sum",
        "slug": "combination-sum",
        "difficulty": "MEDIUM",
        "description": """Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.""",
        "examples": """Example 1:
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.

Example 2:
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:
Input: candidates = [2], target = 1
Output: []""",
        "constraints": """• 1 <= candidates.length <= 30
• 2 <= candidates[i] <= 40
• All elements of candidates are distinct
• 1 <= target <= 40""",
        "topics": ["Array", "Backtracking"],
        "tags": ["Backtracking", "Arrays", "Recursion"],
        "points": 10,
        "acceptance_rate": 69.5,
    },
    {
        "title": "Word Search",
        "slug": "word-search",
        "difficulty": "MEDIUM",
        "description": """Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.""",
        "examples": """Example 1:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true

Example 2:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
Output: true

Example 3:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: false""",
        "constraints": """• m == board.length
• n = board[i].length
• 1 <= m, n <= 6
• 1 <= word.length <= 15
• board and word consists of only lowercase and uppercase English letters""",
        "topics": ["Array", "Backtracking", "Matrix"],
        "tags": ["Backtracking", "Matrix", "DFS"],
        "points": 10,
        "acceptance_rate": 39.7,
    },
    {
        "title": "Sort Colors",
        "slug": "sort-colors",
        "difficulty": "MEDIUM",
        "description": """Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.""",
        "examples": """Example 1:
Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]

Example 2:
Input: nums = [2,0,1]
Output: [0,1,2]""",
        "constraints": """• n == nums.length
• 1 <= n <= 300
• nums[i] is either 0, 1, or 2""",
        "topics": ["Array", "Two Pointers", "Sorting"],
        "tags": ["Arrays", "Two Pointers", "Sorting"],
        "points": 10,
        "acceptance_rate": 60.1,
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "difficulty": "MEDIUM",
        "description": """Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.""",
        "examples": """Example 1:
Input: nums = [1,2,3,4]
Output: [24,12,8,6]

Example 2:
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]""",
        "constraints": """• 2 <= nums.length <= 10^5
• -30 <= nums[i] <= 30
• The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer""",
        "topics": ["Array", "Prefix Sum"],
        "tags": ["Arrays", "Prefix Sum", "Math"],
        "points": 10,
        "acceptance_rate": 64.2,
    },

    # ═══════════════════════════════════════════════════════════
    # HARD PROBLEMS (15 problems)
    # ═══════════════════════════════════════════════════════════
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays",
        "difficulty": "HARD",
        "description": """Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).""",
        "examples": """Example 1:
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.""",
        "constraints": """• nums1.length == m
• nums2.length == n
• 0 <= m <= 1000
• 0 <= n <= 1000
• 1 <= m + n <= 2000
• -10^6 <= nums1[i], nums2[i] <= 10^6""",
        "topics": ["Array", "Binary Search", "Divide and Conquer"],
        "tags": ["Binary Search", "Arrays", "Divide and Conquer"],
        "points": 25,
        "acceptance_rate": 36.2,
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "difficulty": "HARD",
        "description": """Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.""",
        "examples": """Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:
Input: height = [4,2,0,3,2,5]
Output: 9""",
        "constraints": """• n == height.length
• 1 <= n <= 2 * 10^4
• 0 <= height[i] <= 10^5""",
        "topics": ["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
        "tags": ["Arrays", "Two Pointers", "Dynamic Programming", "Stack"],
        "points": 25,
        "acceptance_rate": 57.8,
    },
    {
        "title": "Regular Expression Matching",
        "slug": "regular-expression-matching",
        "difficulty": "HARD",
        "description": """Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
• '.' Matches any single character.
• '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).""",
        "examples": """Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

Example 2:
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.).""",
        "constraints": """• 1 <= s.length <= 20
• 1 <= p.length <= 20
• s contains only lowercase English letters
• p contains only lowercase English letters, '.', and '*'
• It is guaranteed for each appearance of the character '*', there will be a previous valid character to match""",
        "topics": ["String", "Dynamic Programming", "Recursion"],
        "tags": ["Dynamic Programming", "Recursion", "Strings"],
        "points": 25,
        "acceptance_rate": 27.9,
    },
    {
        "title": "Wildcard Matching",
        "slug": "wildcard-matching",
        "difficulty": "HARD",
        "description": """Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:
• '?' Matches any single character.
• '*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).""",
        "examples": """Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

Example 2:
Input: s = "aa", p = "*"
Output: true
Explanation: '*' matches any sequence.

Example 3:
Input: s = "cb", p = "?a"
Output: false
Explanation: '?' matches 'c', but the second letter is 'a', which does not match 'b'.""",
        "constraints": """• 0 <= s.length, p.length <= 2000
• s contains only lowercase English letters
• p contains only lowercase English letters, '?' or '*'""",
        "topics": ["String", "Dynamic Programming", "Greedy", "Recursion"],
        "tags": ["Dynamic Programming", "Strings", "Greedy"],
        "points": 25,
        "acceptance_rate": 26.7,
    },
    {
        "title": "N-Queens",
        "slug": "n-queens",
        "difficulty": "HARD",
        "description": """The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.""",
        "examples": """Example 1:
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above

Example 2:
Input: n = 1
Output: [["Q"]]""",
        "constraints": """• 1 <= n <= 9""",
        "topics": ["Array", "Backtracking"],
        "tags": ["Backtracking", "Arrays", "Recursion"],
        "points": 25,
        "acceptance_rate": 64.1,
    },
    {
        "title": "Merge k Sorted Lists",
        "slug": "merge-k-sorted-lists",
        "difficulty": "HARD",
        "description": """You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.""",
        "examples": """Example 1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6

Example 2:
Input: lists = []
Output: []

Example 3:
Input: lists = [[]]
Output: []""",
        "constraints": """• k == lists.length
• 0 <= k <= 10^4
• 0 <= lists[i].length <= 500
• -10^4 <= lists[i][j] <= 10^4
• lists[i] is sorted in ascending order
• The sum of lists[i].length will not exceed 10^4""",
        "topics": ["Linked List", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort"],
        "tags": ["Linked List", "Heap", "Divide and Conquer"],
        "points": 25,
        "acceptance_rate": 49.3,
    },
    {
        "title": "Reverse Nodes in k-Group",
        "slug": "reverse-nodes-in-k-group",
        "difficulty": "HARD",
        "description": """Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.""",
        "examples": """Example 1:
Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]

Example 2:
Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]""",
        "constraints": """• The number of nodes in the list is n
• 1 <= k <= n <= 5000
• 0 <= Node.val <= 1000""",
        "topics": ["Linked List", "Recursion"],
        "tags": ["Linked List", "Recursion"],
        "points": 25,
        "acceptance_rate": 55.1,
    },
    {
        "title": "Substring with Concatenation of All Words",
        "slug": "substring-with-concatenation-of-all-words",
        "difficulty": "HARD",
        "description": """You are given a string s and an array of strings words. All the strings of words are of the same length.

A concatenated substring in s is a substring that contains all the strings of any permutation of words concatenated.

Return the starting indices of all the concatenated substrings in s. You can return the answer in any order.""",
        "examples": """Example 1:
Input: s = "barfoothefoobarman", words = ["foo","bar"]
Output: [0,9]
Explanation: Since words.length == 2 and words[i].length == 3, the concatenated substring has to be of length 6.
The substring starting at 0 is "barfoo". It is the concatenation of ["bar","foo"] which is a permutation of words.
The substring starting at 9 is "foobar". It is the concatenation of ["foo","bar"] which is a permutation of words.

Example 2:
Input: s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
Output: []
Explanation: Since words.length == 4 and words[i].length == 4, the concatenated substring has to be of length 16.
There is no substring of length 16 is s that is equal to the concatenation of any permutation of words.
We return an empty array.

Example 3:
Input: s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
Output: [6,9,12]
Explanation: Since words.length == 3 and words[i].length == 3, the concatenated substring has to be of length 9.
The substring starting at 6 is "foobarthe". It is the concatenation of ["foo","bar","the"] which is a permutation of words.
The substring starting at 9 is "barthefoo". It is the concatenation of ["bar","the","foo"] which is a permutation of words.
The substring starting at 12 is "thefoobar". It is the concatenation of ["the","foo","bar"] which is a permutation of words.""",
        "constraints": """• 1 <= s.length <= 10^4
• 1 <= words.length <= 5000
• 1 <= words[i].length <= 30
• s and words[i] consist of lowercase English letters""",
        "topics": ["Hash Table", "String", "Sliding Window"],
        "tags": ["Hashing", "Sliding Window", "Strings"],
        "points": 25,
        "acceptance_rate": 32.4,
    },
    {
        "title": "Longest Valid Parentheses",
        "slug": "longest-valid-parentheses",
        "difficulty": "HARD",
        "description": """Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.""",
        "examples": """Example 1:
Input: s = "(()"
Output: 2
Explanation: The longest valid parentheses substring is "()".

Example 2:
Input: s = ")()())"
Output: 4
Explanation: The longest valid parentheses substring is "()()".

Example 3:
Input: s = ""
Output: 0""",
        "constraints": """• 0 <= s.length <= 3 * 10^4
• s[i] is '(', or ')'""",
        "topics": ["String", "Dynamic Programming", "Stack"],
        "tags": ["Dynamic Programming", "Stack", "Strings"],
        "points": 25,
        "acceptance_rate": 32.1,
    },
    {
        "title": "Minimum Window Substring",
        "slug": "minimum-window-substring",
        "difficulty": "HARD",
        "description": """Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.""",
        "examples": """Example 1:
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

Example 2:
Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.

Example 3:
Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.""",
        "constraints": """• m == s.length
• n == t.length
• 1 <= m, n <= 10^5
• s and t consist of uppercase and lowercase English letters""",
        "topics": ["Hash Table", "String", "Sliding Window"],
        "tags": ["Sliding Window", "Hashing", "Strings"],
        "points": 25,
        "acceptance_rate": 39.8,
    },
    {
        "title": "Edit Distance",
        "slug": "edit-distance",
        "difficulty": "HARD",
        "description": """Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:
• Insert a character
• Delete a character
• Replace a character""",
        "examples": """Example 1:
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation: 
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')

Example 2:
Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation: 
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')""",
        "constraints": """• 0 <= word1.length, word2.length <= 500
• word1 and word2 consist of lowercase English letters""",
        "topics": ["String", "Dynamic Programming"],
        "tags": ["Dynamic Programming", "Strings"],
        "points": 25,
        "acceptance_rate": 52.9,
    },
    {
        "title": "Largest Rectangle in Histogram",
        "slug": "largest-rectangle-in-histogram",
        "difficulty": "HARD",
        "description": """Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.""",
        "examples": """Example 1:
Input: heights = [2,1,5,6,2,3]
Output: 10
Explanation: The above is a histogram where width of each bar is 1.
The largest rectangle is shown in the red area, which has an area = 10 units.

Example 2:
Input: heights = [2,4]
Output: 4""",
        "constraints": """• 1 <= heights.length <= 10^5
• 0 <= heights[i] <= 10^4""",
        "topics": ["Array", "Stack", "Monotonic Stack"],
        "tags": ["Stack", "Arrays", "Monotonic Stack"],
        "points": 25,
        "acceptance_rate": 40.2,
    },
    {
        "title": "Word Ladder",
        "slug": "word-ladder",
        "difficulty": "HARD",
        "description": """A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
• Every adjacent pair of words differs by a single letter.
• Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
• sk == endWord

Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.""",
        "examples": """Example 1:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> "cog", which is 5 words long.

Example 2:
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.""",
        "constraints": """• 1 <= beginWord.length <= 10
• endWord.length == beginWord.length
• 1 <= wordList.length <= 5000
• wordList[i].length == beginWord.length
• beginWord, endWord, and wordList[i] consist of lowercase English letters
• beginWord != endWord
• All the words in wordList are unique""",
        "topics": ["Hash Table", "String", "Breadth-First Search"],
        "tags": ["BFS", "Graph", "Strings"],
        "points": 25,
        "acceptance_rate": 36.9,
    },
    {
        "title": "Sliding Window Maximum",
        "slug": "sliding-window-maximum",
        "difficulty": "HARD",
        "description": """You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.

Return the max sliding window.""",
        "examples": """Example 1:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation: 
Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

Example 2:
Input: nums = [1], k = 1
Output: [1]""",
        "constraints": """• 1 <= nums.length <= 10^5
• -10^4 <= nums[i] <= 10^4
• 1 <= k <= nums.length""",
        "topics": ["Array", "Queue", "Sliding Window", "Heap (Priority Queue)", "Monotonic Queue"],
        "tags": ["Sliding Window", "Queue", "Heap"],
        "points": 25,
        "acceptance_rate": 45.6,
    },
    {
        "title": "Basic Calculator",
        "slug": "basic-calculator",
        "difficulty": "HARD",
        "description": """Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().""",
        "examples": """Example 1:
Input: s = "1 + 1"
Output: 2

Example 2:
Input: s = " 2-1 + 2 "
Output: 3

Example 3:
Input: s = "(1+(4+5+2)-3)+(6+8)"
Output: 23""",
        "constraints": """• 1 <= s.length <= 3 * 10^5
• s consists of digits, '+', '-', '(', ')', and ' '
• s represents a valid expression
• '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid)
• '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid)
• There will be no two consecutive operators in the input
• Every number and running calculation will fit in a signed 32-bit integer""",
        "topics": ["Math", "String", "Stack", "Recursion"],
        "tags": ["Stack", "Strings", "Math"],
        "points": 25,
        "acceptance_rate": 40.9,
    },
]




class Command(BaseCommand):
    help = "Import problems into database"

    def handle(self, *args, **kwargs):
        count = 0

        for p in PROBLEMS:
            Problem.objects.update_or_create(
                slug=p["slug"],
                defaults={
                    "title": p["title"],
                    "difficulty": p["difficulty"],
                    "description": p["description"],
                    "examples": p["examples"],
                    "constraints": p["constraints"],
                    "topics": p["topics"],
                    "tags": p["tags"],
                    "points": p["points"],
                    "acceptance_rate": p["acceptance_rate"],
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} problems imported successfully!"))