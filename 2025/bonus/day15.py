from collections import defaultdict, deque
import functools
import re
import heapq

sample_input_1 = '''receive 4
receive 9
receive 2
receive 9
request
request
receive 99999
request
request
'''

debug = True

with open('day15.input') as f:
    lines = f.read().strip().split('\n')
    
if debug:
    lines = sample_input_1.strip().split('\n')
    print(lines)
    
class median_heap:
    def __init__(self):
        self.lo = []  # max heap
        self.hi = []  # min heap

    def add_num(self, num):
        
        heapq.heappush(self.lo, -num)
        if (self.lo and self.hi and (-self.lo[0] > self.hi[0])):
            val = -heapq.heappop(self.lo)
            heapq.heappush(self.hi, val)
        if len(self.lo) > len(self.hi) + 1:
            val = -heapq.heappop(self.lo)
            heapq.heappush(self.hi, val)
        if len(self.hi) > len(self.lo) + 1:
            val = heapq.heappop(self.hi)
            heapq.heappush(self.lo, -val)

    def pop_median(self):
        if len(self.lo) > len(self.hi):
            return -heapq.heappop(self.lo)
        else:
            return heapq.heappop(self.hi)
        
med_heap = median_heap()
counter = 1
ans = 0
for instr in lines:
    if 'receive' in instr:
        num = int(instr.split()[1])
        med_heap.add_num(num)
    else:
        median = med_heap.pop_median()
        ans += median * counter
        counter += 1
        
print(ans)


class median_heap_with_freq:
    def __init__(self):
        self.lo = []  # max heap
        self.hi = []  # min heap
        self.lo_count = 0
        self.hi_count = 0
        
    def add_num(self, num, freq):
        heapq.heappush(self.lo, (-num, freq))
        self.lo_count += freq
        if (self.lo and self.hi and (-self.lo[0][0] > self.hi[0][0])):
            val, val_freq = heapq.heappop(self.lo)
            val = -val
            heapq.heappush(self.hi, (val, val_freq))
            self.lo_count -= val_freq
            self.hi_count += val_freq
        while self.hi_count > self.lo_count + 1:
            val, val_freq = heapq.heappop(self.hi)
            heapq.heappush(self.lo, (-val, val_freq))
            self.hi_count -= val_freq
            self.lo_count += val_freq
        while self.lo_count > self.hi_count + 1:
            val, val_freq = heapq.heappop(self.lo)
            val = -val
            heapq.heappush(self.hi, (val, val_freq))
            self.lo_count -= val_freq
            self.hi_count += val_freq
        
    def pop_median(self):
        ans = None
        if self.lo_count > self.hi_count:
            val, val_freq = heapq.heappop(self.lo)
            val = -val
            if val_freq > 1:
                heapq.heappush(self.lo, (-val, val_freq - 1))
            self.lo_count -= 1
            ans = val
        else:
            val, val_freq = heapq.heappop(self.hi)
            if val_freq > 1:
                heapq.heappush(self.hi, (val, val_freq - 1))
            self.hi_count -= 1
            ans = val
        return ans
    
med_heap = median_heap_with_freq()

counter = 1
ans = 0
for instr in lines:
    if 'receive' in instr:
        num = int(instr.split()[1])
        med_heap.add_num(num, num)
    else:
        median = med_heap.pop_median()
        ans += median * counter
        counter += 1
        
print(ans)