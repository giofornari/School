class Solution(object):
    def twoSum(self, nums, target):
        hashmap = {} #crei la mappa di indici {"numero":suoindice,"2":0}
        for i in range(len(nums)):
            hashmap[nums[i]] = i #hashmap numero : indice
        for i in range(len(nums)):
            complement = target - nums[i] #trova numero complementare
            if complement in hashmap and hashmap[complement] != i: #se il complemento è in numeri e non ha lo stesso indice del primo
                return [i, hashmap[complement]] #array di indici
        return []
