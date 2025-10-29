from numpy import array, add, cos, exp, pi, sin, sqrt, subtract, tan
from random import uniform
from matplotlib.pyplot import subplots

class Particle:
  def __init__(self, init_pos, init_fitness, init_velocity) -> None:
    self.pos, self.v, self.best_fitness, self.best_pos = array(init_pos), array(init_velocity), init_fitness, init_pos
    
# Functions f and g
class Functions:
  @staticmethod
  def all_functions(pos, Function):
      return Functions.f(pos = pos) if Function == 'f' else Functions.g(pos = pos)

  @staticmethod
  def check_best(new_fitness, which_fun, best):
    if which_fun == 'f':
        return True if new_fitness > best else None
      
    if which_fun == 'g':
        return True if new_fitness < best else None
    
    return False

  @staticmethod
  def g(pos):
    x , y = pos[0], pos[1]
    return x * sin(y / x) / (1 + cos(y / x)) * sin(pi * cos(x) * tan(y))

  @staticmethod
  def f(pos):
    x , y = pos[0], pos[1]
    return abs(sin(x) * cos(y) * exp(abs(1 - (sqrt(x ** 2 + y ** 2) / pi))))

# PSO Class Initialization
class PSO:
  def __init__(self, w, c_b, c_g, n, iter, v_limit, function, pos_limit, rand_limit) -> None:
      self.w, self.c_b, self.c_g, self.n, self.iter, self.v_limit, self.pos_limit, self.rand_limit, self.function, self.all_best_results, self.all_particles, self.swarm, self.global_best_pos, self.global_best_fitness = w, c_b, c_g, n, iter, v_limit, pos_limit, rand_limit, function, [], [], [], array([0,0]), 0
      
  def init_particles(self):
    for i in range(self.n):
      pos = array([uniform(-self.pos_limit, self.pos_limit), uniform(-self.pos_limit, self.pos_limit)])
      """
      for fun g
      while(pos[0] == 0):
        pos[0] = uniform(-self.pos_limit, self.pos_limit)
      """
      Fitness = Functions.all_functions(pos, self.function)
      newPart = Particle(init_pos = pos, init_fitness = Fitness, init_velocity = array([uniform(-self.v_limit, self.v_limit), uniform(-self.v_limit, self.v_limit)]))
      if Functions.check_best(new_fitness = Fitness, which_fun = self.function, best = self.global_best_fitness):
        self.global_best_fitness, self.global_best_pos = newPart.best_fitness, newPart.best_pos
      self.swarm.append(newPart)
  
  def move_particle(self, part: Particle):
    r_2 = uniform(0, self.rand_limit)
    part.pos = add(add(add(part.v.dot(self.w), (subtract(part.best_pos , part.pos)).dot(uniform(0, self.rand_limit) * self.c_b)), (subtract(self.global_best_pos , part.pos)).dot(uniform(0, self.rand_limit)*self.c_g)), part.pos)
    part = self.still_within_range(part)
    newFitness = Functions.all_functions(part.pos, self.function)
    if Functions.check_best(new_fitness = newFitness, which_fun = self.function, best = part.best_fitness):
          part.best_fitness, part.best_pos= Functions.all_functions(part.pos, self.function), part.pos     
    return part

  def still_within_range(self, part: Particle):
    part.pos[0], part.pos[1] = self.min_change(self.max_change(part.pos[0])), self.min_change(self.max_change(part.pos[1]))
    """
    for fun g
    while(part.pos[0] == 0):
      part.pos[0] = uniform(-self.pos_limit, self.pos_limit)

    part.pos[0], part.pos[1]= max(-self.pos_limit, min(self.pos_limit, part.pos[0])), max(-self.pos_limit, min(self.pos_limit, part.pos[1]))
    """
    return part

  def max_change(self, x):
    return -((-x) % self.pos_limit) if x > self.pos_limit else x

  def min_change(self, x):
    return -(x % self.pos_limit) if x < -self.pos_limit else x

  def save_positions(self):
    X, Y = [], []
    for i in range(len(self.swarm)):
      X.append(self.swarm[i].pos[0])
      Y.append(self.swarm[i].pos[1])
    self.all_particles.append([X, Y])

  def PSO_iterations(self):
    self.init_particles()
    self.all_best_results, self.all_particles = [], []
    for i in range(self.iter):
      self.all_best_results.append(self.global_best_fitness)
      self.save_positions()
      for i in range(self.n):
        self.swarm[i] = self.move_particle(self.swarm[i])
        new_fitness = Functions.all_functions(self.swarm[i].pos, self.function)
        if Functions.check_best(new_fitness = new_fitness, which_fun = self.function, best = self.global_best_fitness):
          self.global_best_fitness = self.swarm[i].best_fitness
          self.global_best_pos = self.swarm[i].best_pos
          
    self.all_best_results.append(self.global_best_fitness)
    self.save_positions()
    print(self.global_best_pos)
    print(self.global_best_fitness)
    return self.all_best_results

class Display:
  @staticmethod
  def displayParticles(Swarms):
    plot_info, plots = subplots(3, 3)
    plot_info.set_size_inches(30, 20)
    print(len(Swarms))
    for Swarm in range(9):
      """
      all_x, all_y = [], []
      print(Swarms[Swarm])
      for j in range(len(Swarms[Swarm])):
        all_x.append(Swarms[Swarm][j].pos[0])
        all_y.append(Swarms[Swarm][j].pos[1])
      """
      plots[Swarm // 3, Swarm % 3].scatter( Swarms[Swarm * 10][0], Swarms[Swarm * 10][1])

fTest = PSO(w = 0.1, c_b = 10, c_g = 5, n = 200, iter = 100, v_limit = 5, function = 'f', pos_limit = 10, rand_limit = 10)
fResult = fTest.PSO_iterations()

# Display
Display.displayParticles(fTest.all_particles)

gTest = PSO(w = 0.1, c_b = 100, c_g = 100, n = 2000000, iter = 10, v_limit = 100, function = 'g', pos_limit = 100, rand_limit = 10)
gResult = gTest.PSO_iterations()
