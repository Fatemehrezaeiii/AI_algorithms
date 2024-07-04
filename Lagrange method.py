def lagrange(x, y, alpha):
    #Calculating the approximate value using the Lagrange interpolation method
    result = 0
    for i in range(n):
        res = y[i]
        for j in range(n):
            if i != j:
                res *= (alpha - x[j]) /(x[i] - x[j])
                if res == -0.0:  res = 0.0
        print("y{}*L{}({}):".format(i,i,alpha), res)
        result += res
    print("calculating (f({}) = y0*l0({}) + ... + yn*ln({})) ...".format(alpha,alpha,alpha))
    print("Approximate value using Lagrange interpolation method: f({}) = ".format(alpha), result)


def derivative(x, y,h):
    for i in range(n-1):
        print("f'(x{}):".format(i),((y[i+1] - y[i])/h))
    for i in range(n-2):
        print("f''(x{}):".format(i),((1 /( 2 * h))*(-1 * y[i+2] + 4 * y[i+1] - 3 * y[i])))




x_components = []
y_components = []
n = 0

while True:
    try:   #checking whether input is integer or not
        n = int(input("Enter the number of points: "))
        if n > 0:
            break
        else:
            print("invalid entry, Try again.")
    except ValueError:
        print("invalid entry, Try again.")

for i in range(n):
    while True:
        try:
            x_entry = (float(input("enter x{}: ".format(i))))
            x_components.append(x_entry)
            break
        except ValueError:
            print("invalid entry, Try again.")

for j in range(n):
    while True:
        try:
            y_entry = (float(input("enter y{}: ".format(j))))
            y_components.append(y_entry)
            break
        except ValueError:
            print("invalid entry, Try again.")

alpha = 0
while True:
    try:   #checking whether alpha is float or not
        alpha = float(input("Enter the value of alpha: ")) #Getting alpha
        break
    except ValueError:
        print("invalid entry, Try again.")
lagrange(x_components, y_components, alpha)   #Calling the Lagrange interpolation function

for i in range(0,n-1):
    h = x_components[1] - x_components[0]
    if x_components[i + 1] - x_components[i] != h:
        print("The points are not equidistant")
        break
    elif i + 1 == n - 1 :
        derivative(x_components,y_components,h)
