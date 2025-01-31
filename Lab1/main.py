from fastapi import FastAPI 


app = FastAPI()

@app.get("/factorial/{starting_number}")
def compute_factorial(starting_number: int):
    if starting_number == 0:
        
        return {"factorial": False} 
    result = 1
    num = starting_number

    while num > 1:
        result *= num
        num -= 1

    return {"factorial": result}  