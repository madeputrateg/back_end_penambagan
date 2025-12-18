import pickle


class testing():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    

    def pred(self,data):
        klk = data["x"]
        return (klk - self.x ) * self.y
    
data = testing(10,20)



with open("C:\\Users\\putra\\Downloads\\fileuplaod\\tester.pkl","wb") as file:
    pickle.dump(data,file)