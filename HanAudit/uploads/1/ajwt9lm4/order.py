# -*- coding:utf-8 -*-

li = [13,22,6,11,99] 
for n in range(1,len(li)):
	# 1,2,3,4
	#len(li)-n
	# 4,3,2,1
	for m in range(len(li)-n): #4,3,2,1
		# 获取第m个值
		num1 = li[m]
		# 获取第m+1个值
		num2 = li[m+1]
		if num1 > num2:
			# 将较大的值放在右侧
			temp = li[m]
			li[m] = num2
			li[m+1] = temp
print li