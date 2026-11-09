import struct,zlib,pathlib,json
class NBT:
 def __init__(self,b): self.b=b; self.i=0
 def take(self,n): v=self.b[self.i:self.i+n]; self.i+=n; return v
 def num(self,f): return struct.unpack('>'+f,self.take(struct.calcsize('>'+f)))[0]
 def text(self): return self.take(self.num('H')).decode('utf8')
 def tag(self,t):
  if t in [1,2,3,4,5,6]: return self.num({1:'b',2:'h',3:'i',4:'q',5:'f',6:'d'}[t])
  if t==7: return self.take(self.num('i'))
  if t==8: return self.text()
  if t==9:
   typ=self.num('B'); n=self.num('i'); return [self.tag(typ) for _ in range(n)]
  if t==10:
   d={}
   while True:
    typ=self.num('B')
    if not typ:return d
    name=self.text();d[name]=self.tag(typ)
  if t in [11,12]: return [self.num('i' if t==11 else 'q') for _ in range(self.num('i'))]
  raise ValueError(t)
def read(path):
 b=zlib.decompress(path.read_bytes(),31); n=NBT(b);assert n.num('B')==10;n.text();d=n.tag(10);assert n.i==len(b);return d
