import pickle


class testing2():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    

    def pred(self,data):
        x = data["x"]
        return (x + self.x ) * self.y
    
data = testing2(10,20)


with open("C:\\Users\\putra\\Downloads\\fileuplaod\\testertwo.pkl","wb") as file:
    pickle.dump(data,file)