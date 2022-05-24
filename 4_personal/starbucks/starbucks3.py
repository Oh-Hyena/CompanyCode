class Starbucks():
    name = "제품 이름"
    info = "제품 정보"
    kcal = "제품 열량"       
     
     
class coffee(Starbucks):
    def __init__(self, name, info, kcal, cost):
        super().__init__(name, info, kcal)
        # self.name = name
        # self.info = info
        # self.kcal = kcal
        self.cost = cost
        
    
    def coffee_show(self):
        print(f"제품 이름 : {self.name}")
        print(f"제품 설명 : {self.info}")
        print(f"제품 열량 : {self.kcal}")
        print(f"제품 가격 : {self.cost}")
        print()
        
        
class food(Starbucks):
    def __init__(self, name, info, kcal, cost):
        self.name = name
        self.info = info
        self.kcal = kcal
        self.cost = cost
        
    
    def food_show(self):
        print(f"제품 이름 : {self.name}")
        print(f"제품 설명 : {self.info}")
        print(f"제품 열량 : {self.kcal}")
        print(f"제품 가격 : {self.cost}")
        print()


if __name__ == "__main__":
    COFFEE = coffee("아메리카노", "americano", 0, 1500)
    COFFEE.coffee_show()
    
    FOOD = food("샌드위치", "sandwich", 300, 4500)
    FOOD.food_show()
