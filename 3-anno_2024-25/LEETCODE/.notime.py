# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        for i in range(max(len(l1), len(l2))):
            newlist[i] = (l1[i] if l1[i] != 0 else 0)+(l2[i]  if l2[i] != 0 else 0)
        
