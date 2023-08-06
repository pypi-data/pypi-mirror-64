## A package as a complement for statistic computation
 
### Usage
```python
from stat_complement import HotellingT2,JaccobiSolve

X=np.array([[-3,15],[4,16],[5,11]])
mu=np.array([[4,14]])
HotellingT2(X,mu)

# x: initial point delta: stop criteria
JaccobiSolve(A,b,x,delta)


