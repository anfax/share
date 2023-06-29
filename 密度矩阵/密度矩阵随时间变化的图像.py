import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the constants
I = 1.0e-46 # rotational inertia in kg*m^2
hbar = 6.626e-34 / (2*np.pi) # reduced Planck constant in J*s
E_1 = hbar**2 / (2*I) # rotational energy level for J=1 in J

# Define the initial density matrix in the |Y_JM> basis
rho_0 = np.array([[1, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0],
                  [0, 0, 1, 0, 0],
                  [0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0]]) / 4

# Define the time evolution function for the density matrix
def rho_t(t):
    # Return the density matrix at time t
    return np.diag([1, np.exp(-1j*E_1*t/hbar), np.exp(-1j*E_1*t/hbar), np.exp(-1j*E_1*t/hbar), 0]) @ rho_0 @ np.diag([1, np.exp(1j*E_1*t/hbar), np.exp(1j*E_1*t/hbar), np.exp(1j*E_1*t/hbar), 0])

# Define the function to convert complex numbers to colors
def complex_to_rgb(z):
    # Return the RGB color for a complex number z
    # Use hue to represent angle, brightness to represent magnitude
    hue = np.angle(z) / (2*np.pi) % 1 # map angle to [0, 1]
    brightness = np.clip(np.abs(z), 0, 1) # clip magnitude to [0, 1]
    return plt.cm.hsv(hue, brightness) # use hsv colormap

# Define the function to plot the density matrix as an image
def plot_rho(rho):
    # Plot the density matrix as an image
    # Use complex_to_rgb to convert each element to a color
    img = np.zeros((rho.shape[0], rho.shape[1], 3)) # initialize an empty image
    for i in range(rho.shape[0]):
        for j in range(rho.shape[1]):
            img[i,j,:] = complex_to_rgb(rho[i,j]) # assign the color for each pixel
    plt.imshow(img) # show the image
    plt.xticks(range(5), ['$|Y_{00}\\rangle$', '$|Y_{1-1}\\rangle$', '$|Y_{10}\\rangle$', '$|Y_{11}\\rangle$', '$|Y_{2-2}\\rangle$']) # label the x-axis
    plt.yticks(range(5), ['$\\langle Y_{00}|$', '$\\langle Y_{1-1}|$', '$\\langle Y_{10}|$', '$\\langle Y_{11}|$', '$\\langle Y_{2-2}|$']) # label the y-axis
    plt.title('Density matrix') # add a title

# Define the animation function
def animate(t):
    # Animate the density matrix at time t
    plt.clf() # clear the previous plot
    plot_rho(rho_t(t)) # plot the current density matrix

# Create a figure and an animation
fig = plt.figure()
ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 10e-12, 100), interval=100)
plt.show()