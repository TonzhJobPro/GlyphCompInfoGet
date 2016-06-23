import sys, codecs, os
#Ver4：修改缩放变化率判断逻辑
f_out = codecs.open(fl.font.font_name + 'ComponentInfo_CompToChar_ScaleSortedrenren.txt', 'w', 'utf-8')

def readnewfiles(input_file_name):
	is_unicode = False
	f_in = open(input_file_name, 'r')
	input_list = []
	

	text = f_in.read()
	for encoding_way in ['ascii','gbk','utf-8','utf-16','utf-16-le', 'utf-16-be']:
		try:
			text = text.decode(encoding_way)
			break
		except UnicodeDecodeError:
			continue
		except:
			print '无法读取输入文件，请检查！'
			sys.exit()
			

	lines = text.splitlines()
	for line in lines:
		line = line.replace('\r', '')
		line = line.replace('\n', '')
		line = line.replace(' ', '')
		line = line.strip()
		if '0x' in line or '0X' in line:
			is_unicode = True
		if is_unicode:
			input_list.append(str(line))
		else:
			for char in line:
				input_list.append(hex(ord(char)))
	return 	input_list

#input_file_name = '6763unicode.txt'
#input_file_name = "Kr_Cn1798.txt"	
 
RL_file_list = readnewfiles('RL.txt') #左右结构字表
UD_file_list = readnewfiles('UD.txt') #上下结构字表

fl.Unselect()
glyphs = fl.font.glyphs
sums = 0

comps = {}
for g in glyphs:
	complist = g.components
	if len(complist) != 0:
		#f_out.write(unichr(int(hex(g.unicode), 16)) + "\t" + (hex(g.unicode)) + "\t" + str(g.index) + "\t")
		#Version3 组件排序
		for com in complist:
			#com_g = glyphs[com.index]
			if comps.has_key(com.index):
				val = comps[com.index]
				val.append((com,g))	
			else:
				comps[com.index] = [(com,g)]
			#f_out.write(unichr(int(hex(com_g.unicode), 16)) + "\t" + (hex(com_g.unicode)) + "\t" + str(com_g.index)+ "\t")
		#f_out.write('\r\n')
comps1= sorted(comps.iteritems(), key=lambda d:d[0])

for key,val in comps1:
	com_g = glyphs[key]
	f_out.write(unichr(int(hex(com_g.unicode), 16)) + "\t" + str(com_g.index)+ "\t")
	val_sorted = check_scale(key,val)
	#price_id = len(val_sorted)/2
	#f_out.write(unichr(int(hex(val_sorted[price_id][1].unicode), 16)) + "\t")
	for gscale,g in val_sorted:
		f_out.write(unichr(int(hex(g.unicode), 16)) + "\t")
	f_out.write('\r\n')
f_out.close()		
 #http://www.e-font.de/flpydoc/
