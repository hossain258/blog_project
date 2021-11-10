class FirstClass:

    def function_1(self):
        print("Inside Function 1")

    def function_2(self):
        print("Inside Function 2")


class SecondClass(FirstClass):

    def function_1(self):
        print("In second class function 1")
        super().function_2()
        super().function_1()
        self.super_function()

    def super_function(self):
        print(1234)



instance_1 = SecondClass()
instance_1.function_1()


