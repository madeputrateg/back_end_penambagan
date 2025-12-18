import pickle


class testing4():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    

    def pred(self,data):
        x = data["x"]
        y = data["y"]
        return (x - self.x ) / self.y
    
data = testing4(10,20)



with open("C:\\Users\\putra\\Downloads\\fileuplaod\\testerfourth.pkl","wb") as file:
    pickle.dump(data,file)