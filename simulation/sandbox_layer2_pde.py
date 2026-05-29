import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

class BiologicalWorldModelSandbox:
    """
    Layer 2 Sandbox: Moving from symbolic CA to biophysically constrained PDEs.
    Simulating a tumor cross-section with nutrient/oxygen diffusion and cellular consumption.
    """
    def __init__(self, size=100, dt=0.01, dx=1.0):
        self.size = size
        self.dt = dt
        self.dx = dx
        
        # State grids
        # 1. Oxygen concentration (0 to 1)
        self.oxygen = np.ones((size, size))
        
        # 2. Tumor cell density (0 to 1)
        self.tumor_cells = np.zeros((size, size))
        
        # Initialize a small tumor cluster in the center
        cx, cy = size // 2, size // 2
        r = 5
        y, x = np.ogrid[-cx:size-cx, -cy:size-cy]
        mask = x**2 + y**2 <= r**2
        self.tumor_cells[mask] = 1.0

        # Diffusion coefficient for oxygen
        self.D_O2 = 0.2
        # Consumption rate of oxygen by tumor cells
        self.consume_rate = 0.5
        # Threshold of oxygen below which hypoxia occurs (necrosis/angiogenesis trigger)
        self.hypoxia_threshold = 0.3
        
        # Cellular Automata / PDE hybrid update
        self.tumor_proliferation_rate = 0.1

    def solve_diffusion(self):
        """
        Simple Finite Difference Method for 2D Diffusion Equation:
        dU/dt = D * Laplace(U) - Consumption(U, Cells)
        """
        # Laplace operator using 5-point stencil
        laplace_O2 = (
            np.roll(self.oxygen, 1, axis=0) + np.roll(self.oxygen, -1, axis=0) +
            np.roll(self.oxygen, 1, axis=1) + np.roll(self.oxygen, -1, axis=1) -
            4 * self.oxygen
        ) / (self.dx**2)
        
        # Boundaries: fixed oxygen supply at edges (e.g. vasculature)
        laplace_O2[0,:] = 0
        laplace_O2[-1,:] = 0
        laplace_O2[:,0] = 0
        laplace_O2[:,-1] = 0

        # Oxygen decreases based on tumor cell density
        consumption = self.consume_rate * self.tumor_cells * self.oxygen
        
        # Update oxygen
        self.oxygen += self.dt * (self.D_O2 * laplace_O2 - consumption)
        
        # Enforce boundary conditions (constant supply at edges)
        self.oxygen[0,:] = 1.0
        self.oxygen[-1,:] = 1.0
        self.oxygen[:,0] = 1.0
        self.oxygen[:,-1] = 1.0
        self.oxygen = np.clip(self.oxygen, 0, 1)

    def solve_cellular_dynamics(self):
        """
        Update tumor density based on available oxygen.
        """
        # Proliferation where oxygen is sufficient
        proliferation = self.tumor_proliferation_rate * self.tumor_cells * (1 - self.tumor_cells)
        # Suppress proliferation in hypoxia
        proliferation[self.oxygen < self.hypoxia_threshold] = -0.05 * self.tumor_cells[self.oxygen < self.hypoxia_threshold]
        
        # Spatial expansion (gradient driven)
        # Cells migrate slightly towards higher oxygen (chemotaxis proxy)
        
        self.tumor_cells += self.dt * proliferation
        self.tumor_cells = np.clip(self.tumor_cells, 0, 1)

    def step(self):
        self.solve_diffusion()
        self.solve_cellular_dynamics()

def run_simulation(steps=500):
    model = BiologicalWorldModelSandbox(size=50)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    im1 = ax1.imshow(model.oxygen, cmap='Blues', vmin=0, vmax=1)
    ax1.set_title('Oxygen Gradient (PDE)')
    
    im2 = ax2.imshow(model.tumor_cells, cmap='Reds', vmin=0, vmax=1)
    ax2.set_title('Tumor Density')
    
    def update(frame):
        for _ in range(10):  # 10 PDE steps per visual frame
            model.step()
        im1.set_array(model.oxygen)
        im2.set_array(model.tumor_cells)
        return [im1, im2]
    
    print("Simulating Layer 2 Biological PDEs...")
    anim = FuncAnimation(fig, update, frames=steps//10, interval=50, blit=True)
    
    # Save the output
    os.makedirs('reports', exist_ok=True)
    anim.save('reports/layer2_pde_tumor_ecology.gif', writer='pillow')
    print("Simulation saved to reports/layer2_pde_tumor_ecology.gif")

if __name__ == "__main__":
    run_simulation(steps=200)
