message = "aBHAY:@private Karthik hey how are toy"
user = message.split(":")[0]
action = message.split(":")[1].split(" ")[0]
friendName = message.split(":")[1].split(" ")[1]
message = message.split(":")[1].split(" ",1)[1]
print(user,action)
print("firned name = ",friendName)
print("Message = ",message)