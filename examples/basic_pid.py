import ctrlbench

gains = ctrlbench.PidGains(kp=2.0, ki=0.5, kd=0.1)
plant = ctrlbench.PlantConfig(response=0.7, disturbance=0.0)
profile = ctrlbench.ProfileConfig(10.0, 10.0, 10.0)

sim = ctrlbench.Simulator(gains=gains, plant=plant, profile=profile)
result = sim.run(start=0, end=100)
