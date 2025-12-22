import pickle


class testing5():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    

    def pred(self,data):
        x = data["age"]
        y = data["thalach"]
        return (x - self.x ) / self.y + y*0.2
    
data = testing5(10,20)



with open("C:\\Users\\putra\\Downloads\\fileuplaod\\testerfive.pkl","wb") as file:
    pickle.dump(data,file)