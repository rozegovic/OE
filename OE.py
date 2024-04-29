from cmath import inf
from doctest import SkipDocTestCase
from unittest import skip
import numpy as np
import matplotlib.pyplot as plt
 
def first(the_iterable):
  ff = []
  for i in the_iterable:
    ff.append(i[0])
  return ff   
  
def last(the_iterable):
  ff = []
  for i in the_iterable:
    ff.append(i[-1])
  return ff 
            
            
def normalize(x):
 
  return np.array(x) / np.linalg.norm(x)
 
def plot_scene(object_list, **kwargs):
  
  fig = plt.figure(**kwargs)
  plt.rc('axes', axisbelow=True)
  plt.grid(color='0.95')
  for o in object_list:
    
    _plot_object(fig, o)
 
   
  return fig
 
def _plot_object(p,wall):
 
  adjacent = np.array([wall.normal_[1], -wall.normal_[0]])
  
  a = wall.position_ + adjacent * 20
  b = wall.position_ - adjacent * 20
 
  y = [a[-1], b[-1]]
  x = [a[0], b[0]]
  line = np.array([x, y])
 
  plt.plot(line[0], line[1], label="Wall")
  
def plot_photon_arrow(p, photon, length=2, **kwargs):
 
  line = np.array([photon.position_, photon.position_ + length*photon.direction_])
  
  plt.arrow(line[0][0], line[0][1],dx=length*photon.direction_[0],
  
  dy=length*photon.direction_[1], color="darkred", shape='full',
  
  zorder=3, lw=2, head_width=0.35, head_length=0.35, length_includes_head=True)
  if "label" in kwargs:
    plt.scatter(photon.position_[0], photon.position_[1],
    
    color="darkred", s=20, zorder=3, label=kwargs["label"])
  else:
    plt.scatter(photon.position_[0], photon.position_[1], color="darkred", s=20, zorder=3)
 
class Wall:
  def __init__(self, p, n):
    self.position_=p
    self.normal_=n
 
box_scene=[Wall([10,0],[-1,0]),Wall([-10,0],[1,0]),Wall([0,10],[0,-1]),Wall([0,-10],[0,1])]
ff=plot_scene(box_scene, figsize=(40,20))
figsize=(400,200)
plt.show()
 
class Photon:
  def __init__(self, p, l, ior):
    self.position_=p
    self.direction_=l
    self.ior_=ior
 
box_scene=[Wall([10,0],[-1,0]),Wall([-10,0],[1,0]),Wall([0,10],[0,-1]),Wall([0,-10],[0,1])]
ff=plot_scene(box_scene, figsize=(40,20))
figsize=(400,200)
photon=Photon([-1.0,1.0],[0.91,-0.6],1.0)
plot_photon_arrow(ff,photon,6)
 
class Intersection:
  def __init__(self, obj, dist, point):
    self.object_=obj
    self.dist_=dist
    self.point_=point
 
class Miss:
  pass
 
def intersection_distance(photon, wall):
  return np.dot(np.array(wall.position_)-np.array(photon.position_),wall.normal_)/
  
  np.dot(photon.direction_,wall.normal_)
 
def intersection(photon, wall, e=1e-3):
  d=intersection_distance(photon, wall)
  if d>e:
    return Intersection(wall,d,photon.position_+np.array(d)*np.array(photon.direction_))
  else:
    return Miss()
 
test_wall=Wall([8,-1], normalize([-3,1]))
ff=plot_scene([test_wall],figsize=(40,20))
dizzy=Photon([0.0,0.0],[0.914068,-0.405561],1.0)
plot_photon_arrow(ff,dizzy,4)
test_intersection=intersection(dizzy,test_wall)
plt.scatter(test_intersection.point_[0], test_intersection.point_[1])
plt.show()
  
def closest_hit(photon, objects):
  array_i=[]
  array_d=[]
  for x in objects:
    if isinstance(intersection(photon,x),Intersection):
      array_i.append(intersection(photon, x))
  for x in array_i:
    array_d.append(x.dist_)  
  i=np.argmin(array_d)
  return array_i[i]
 
test_wall=Wall([8,-1],normalize([-3,1]))
box_scene=[Wall([10,0],[-1,0]),Wall([-10,0],[1,0]),Wall([0,-10],[0,1]),Wall([0,10],[0,-1])]
ex_1_scene=box_scene + [test_wall]
philip=Photon([3,0],normalize([0.5,-1]),1.0)
test_closest=closest_hit(philip,ex_1_scene)
ff=plot_scene(ex_1_scene,figsize=(40,20))
plot_photon_arrow(ff,philip,5)
plt.scatter(test_closest.point_[0], test_closest.point_[1])
plt.show()
 
def reflect(l1,n):
  return l1-2.*np.dot(l1,n)*np.array(n)
 
def interact(photon, hit):
    new_photon=Photon(hit.point_, reflect(photon.direction_, hit.object_.normal_), photon.ior_)
    return new_photon
 
def step_ray(photon, objects):
    hit=closest_hit(photon, objects)
    return interact(photon, hit)     
 
def trace(photon, scene, N):
    array_f=[]
    array_f.append(photon)
    temp=photon
    for x in range(N-1):
        temp=step_ray(temp,scene)
        array_f.append(temp)
    return array_f
 
test_wall=Wall([8,-1],normalize([-3,1]))
box_scene=[Wall([10,0],[-1,0]),Wall([-10,0],[1,0]),Wall([0,10],[0,-1]),Wall([0,-10],[0,1])]
ex_1_scene=box_scene+[test_wall]
philip=Photon([3,0],normalize([.5,-1]),1.0)
mirror_test_ray_N=6
ff=plot_scene(ex_1_scene)
path=trace(philip,ex_1_scene,mirror_test_ray_N)
line=[philip.position_]
line.extend([r.position_ for r in path])
plot_photon_arrow(ff,philip,4)
plt.plot(first(line), last(line), zorder=1, lw=3, color="pink")
for ph in path:
  plot_photon_arrow(ff,ph,4)
plt.show()