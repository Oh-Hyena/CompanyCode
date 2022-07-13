# txt 파일을 읽어서, 전체 이미지 장수, 객체(person, car) 개수, 전체 객체 개수 write 

import os
import sys


txtDir = r"D:\0610\dataset2\total_dataset"
resDir = r"D:\0610\dataset2"

ENCODING_FORMAT = "UTF-8"


class CountObject:
    def checkInitDirValid(self):
        if os.path.isdir(txtDir) is False:
            print(f'[Error] {txtDir} is invalid')
            return False
        if os.path.isdir(resDir) is False:
            print(f'[Error] {resDir} is invalid')
            return False
        return True


    def makeCountResDir(self, resDir):
        if not os.path.isdir(resDir):
            os.makedirs(resDir, exist_ok=True)


    def readFileToList(self, fileName:str):
        fList = []
    
        if os.path.isfile(fileName) is False:
            print(f'[Error] {fileName} is invalid')
            return fList
            
        with open(fileName, 'r', encoding=ENCODING_FORMAT) as rf:
            for eachLine in rf:
                fList.append(eachLine.strip('\n'))

        # print(f'[Done] File Read Done : {fileName}')
        
        return fList
        

    def countObject(self):
        TotalImg   = 0
        txtList    = os.listdir(txtDir)
        TotalImg   = len(txtList)  # 이미지 장수
        
        TotalLen    = 0
        personTotal = 0
        carTotal    = 0
        
        for txtfile in txtList:
            if txtfile.endswith(".txt"):
                totalSrcFilePath    = os.path.join(txtDir, txtfile)
                readList            = self.readFileToList(totalSrcFilePath)
                print("[ Done ] Read Txt File")
                
                TotalLen           += len(readList)  # 전체 객체 개수
                
                for each in readList:
                    eachSplit       = each.split(" ")
                    classes         = eachSplit[0]
                                
                    if classes == '0':
                        personTotal += 1   # person 객체 개수
                    else:
                        carTotal    += 1   # car 객체 개수
                    
                with open(os.path.join(resDir, "analysis_" + os.path.basename(txtDir) + ".txt"), 'w', encoding=ENCODING_FORMAT) as f:
                    f.write(f"[ img count ]\n")
                    f.write(f"* 전체 : {str(TotalImg).rjust(5)}\n")
                    f.write(f"\n[ obj count ]\n")
                    f.write(f"* 사람 : {str(personTotal).rjust(5)}\n")
                    f.write(f"* 차량 : {str(carTotal).rjust(5)}\n")  
                    f.write(f"* 전체 : {str(TotalLen).rjust(5)}\n")  
                
    
    def run(self):
        if self.checkInitDirValid() is False:
                sys.exit(-1)
        self.makeCountResDir(resDir)   
        self.countObject()


if __name__ == "__main__":
    program = CountObject()
    program.run()
