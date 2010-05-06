from Foundation import *
from AppKit import *
import objc
import inspect
from functools import wraps
from types import FunctionType, MethodType
__proxy_cache = {}

IGNORENAMES = 'methodForSelector_'.split()
def MakeSuckNDropProxyClass(cls):
    if cls in __proxy_cache:
        return __proxy_cache[cls]
    
    def tracer(name):
        print "Calling proxied", name
        
    def MakeProxyMethod(f):
        name = f.__name__.replace(':', '_')
        proxies = [
                    lambda self: (tracer(name), getattr(self.obj, name)())[1],
                    lambda self, a1: (tracer(name), getattr(self.obj, name)(a1))[1],
                    lambda self, a1, a2: (tracer(name), getattr(self.obj, name)(a1, a2))[1],
                    lambda self, a1, a2, a3: (tracer(name), getattr(self.obj, name)(a1, a2, a3))[1],
                    lambda self, a1, a2, a3, a4: (tracer(name), getattr(self.obj, name)(a1, a2, a3, a4))[1],
                    lambda self, a1, a2, a3, a4, a5: (tracer(name), getattr(self.obj, name)(a1, a2, a3, a4, a5))[1],
                    lambda self, a1, a2, a3, a4, a5, a6: (tracer(name), getattr(self.obj, name)(a1, a2, a3, a4, a5, a6))[1],
                    lambda self, a1, a2, a3, a4, a5, a6, a7: (tracer(name), getattr(self.obj, name)(a1, a2, a3, a4, a5, a6, a7))[1],
                    lambda self, a1, a2, a3, a4, a5, a6, a7, a8: (tracer(name), getattr(self.obj, name)(a1, a2, a3, a4, a5, a6, a7, a8))[1],
                  ]
        # proxies = map(wraps(f, assigned=['__name__', '__doc__']), proxies)
        #count = name.count('_', 1)
        # count = f.__name__.count(':')
        if isinstance(f, objc.selector):
            count = len(objc.splitSignature(f.signature)) - 3
        else:
            count = len(inspect.getargspec(f)[0])
        # if name.startswith('p_'):
        #     count -= 1
        # if count and not name.endswith('_'):
        #     count -= 1 # e.g. p_foo()
        # print "Proxying", name, "with", count, "arg version"
        # try:
        #     print "signature", objc.splitSignature(f.signature)
        # except:
        #     pass
        return proxies[count]
        
    def ProxyMeta(name, bases, dict):
        assert len(bases) > 0
        name = '%sSuckNDropProxy' % cls.__name__
        flattenedBasesDict = {}
        base = bases[0]
        while base:
            if base in (NSObject, NSControl):
                break
            print "Extending bases with", base.__name__
            flattenedBasesDict.update(base.__dict__)
            base = base.__bases__[0] if base.__bases__ else None
            
        methods = [ (mname, method) for mname, method in flattenedBasesDict.iteritems() 
                        if not mname.startswith('__')
                        and not mname.startswith('init')
                        and not mname.startswith('p_')
                        and not mname.startswith('_pyobjc')
                        and not mname.startswith('pyobjc_')
                        and not "__" in mname
                        and not mname.startswith('QTHUD_')
                        # and not mname.startswith('CI_')
                        and not mname in IGNORENAMES
                        and not mname in dict
                        and isinstance(method, (FunctionType, MethodType, objc.selector, classmethod))]
        count = 0
        for mname, method in methods:
            dict[mname] = MakeProxyMethod(method)
            count +=1
        print "Creating class %s(%s) with %s items" % (name, ','.join(map(str, bases)), len(dict))
        newClass = type(name, bases, dict)
        __proxy_cache[cls] = newClass
        return newClass
    
    class SuckNDropProxy(cls):
        __metaclass__ = ProxyMeta
        
        def __new__(cls, obj, row):
            return cls.alloc().initWithSuckNDropProxyObject_clickedRow_(obj, row)
            
        def initWithSuckNDropProxyObject_clickedRow_(self, obj, row):
            self.obj = obj
            self = super(SuckNDropProxy, self).init()
            if not self:
                return self
            
            self.obj = obj
            self.row = row
            return self
            
        def clickedRow(self):
            print "Proxied clickedRow() ->", self.row
            return self.row
        
        # def itemAtRow_(self, *args):
        #     return self.obj.itemAtRow_(*args)
    
    return SuckNDropProxy

def MakeSuckNDropProxy(obj, clickedRow):
    PClass = MakeSuckNDropProxyClass(obj.__class__)
    return PClass(obj, clickedRow)
    
# print "Made Proxy class"
# P = MakeSuckNDropProxy(NSOutlineView)
# print "Inited"
# v = NSOutlineView.alloc().init()
# p = P(v, 5)

__all__ = 'MakeSuckNDropProxy'.split()