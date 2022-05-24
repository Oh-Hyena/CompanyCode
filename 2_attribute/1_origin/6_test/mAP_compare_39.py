annotation_label = r'E:\dataset\attribute 0329\market_1501\valid_dataset\39class_attribute_annotation\market1501_valid_merge_annotation.txt'
TXTFILE = r'E:\dataset\attribute\0917_result\result_val.txt'
Config_DIR = r'E:\dataset\attribute\0917_result\config.data'
Classes_DIR = r'E:\dataset\attribute\0917_result\39class.name'

classes_merge = []
for index in open(Classes_DIR):
	index = index.replace('\n',"")
	classes_merge.append(index)						#classes
	
with open(annotation_label,'r') as f:
	txt = f.readlines()
	GTload =[line.strip() for line in txt if len(line.strip().split()[0:])]
	
with open(TXTFILE,'r') as f:
	txt = f.readlines()
	RESULTload =[line.strip() for line in txt if len(line.strip().split()[0:])]
	
print(len(GTload ), len(RESULTload))

CLASSNUM = 39
temp = []
GT = []
RESULT = []
AP = [0 for _ in range(CLASSNUM)]
APcount = [0 for _ in range(CLASSNUM)]
AP_prob =[0 for _ in range(CLASSNUM)]
DATANUM = len(GTload)
mAP = 0

for i in range(CLASSNUM):
	for j in range(DATANUM):
		if GTload[j][i] == '1':
			#print(GTload[j][i])
			APcount[i] += 1
			if GTload[j][i] == RESULTload[j][i]:
				#print(GTload[j][i],RESULTload[j][i])
				AP[i] += 1                
	if APcount[i] != 0:
		AP_prob[i] = AP[i] / APcount[i] * 100
	mAP += AP_prob[i]
mAP = mAP / CLASSNUM 
TP = 0
TC = 0
for i in range(CLASSNUM):
	TC += APcount[i]
	TP += AP[i]
map = TP/TC*100
for i in range (CLASSNUM):
    #print('{0}\t:\t{1:.2f}\ttrue count : {2}'.)
    print('%16s %13.3f TP : %13d true count : %13d'%(classes_merge[i],AP_prob[i],AP[i],APcount[i]))

print(TP, TC)
print('All data : ', DATANUM)
print('mAP : ', map)