"""
MyClass uses MyMeta as metaclass
"""

class MyMeta(type):
    def __new__(cls, name, bases, attr):
        """
        Change the attr dict to dynamically add methods and attributes
        """
        print('MyMeta.__new__', cls, name, bases, attr)
        def g1(self):
            print('g1() defined in MyMeta.__new__')
            return self.x * -10
        attr['g1'] = g1
        name += 'Amended' # manipulate class name
        return super().__new__(cls, name, bases, attr)
    
    
    def __init__(cls, name, bases, attr):
        """
        http://stackoverflow.com/questions/1840421/is-there-any-reason-to-choose-new-over-init-when-defining-a-metaclass
        
        If you want to alter the attributes dict before the class is created, 
        or change the bases tuple, you have to use __new__. 
        By the time __init__ sees the arguments, the class object already exists. 
        Also, you have to use __new__ if you want to return something other than 
        a newly created class of the type in question.

        On the other hand, by the time __init__ runs, the class does exist. 
        Thus, you can do things like give a reference to the just-created class 
        to one of its member objects.
        
        __new__ can do everything that __init__ can do, but not the other way around. 
        __init__ can be more convenient to use though
        """
        print('MyMeta.__init__', cls, name, bases, attr)
        # WARNING: this line has NO EFFECT, instantiated class will NOT have g2()!
        attr['g2_no_effect'] = lambda self: self.x * -20
        name = 'RenameClassInInitHasNoEffect'
        super().__init__(name, bases, attr)
        # you can add attrs to class
        cls.g3 = lambda self: self.x * -30
    
    
    def __call__(cls, *args, **kwargs):
        """
        http://stackoverflow.com/a/39363704/3453033
        
        Make sure a method always gets called *after* any subclass's __init__
        metaclass's __call__ calls class's __new__ and then __init__, before 
        it returns a fully created instance

        __call__'s signature: (cls, *obj_init_args and kwargs)
        type.__call__ means an instantiated type is being called: type(...)()
        == a class is being called on args and kwargs
        == an object of that class is being instantiated
        """
        obj = super().__call__(*args, **kwargs)
        print('MyMeta.__call__', obj, 'instantiated')
        # now do anything immediately *after* obj.__init__()
        if cls.__name__ != 'BaseClass': # not base class
            obj.my_after_call() # directly manipulate obj *instance*
            pass
        return obj


class MyClass(metaclass=MyMeta):
    def __new__(cls, *args, **kwargs):
        """
        - https://concentricsky.com/articles/detail/pythons-hidden-new
          explains the incredible power of __new__

        ALWAYS use *args, **kwargs in __new__ signature, because subclasses 
        might have different __init__ parameters.
        
        __new__ is useful when you want to enforce certain properties even when
        your subclasses forget to call super().__init__()
        """
        print('MyClass.__new__', cls, args, kwargs)
        obj = super().__new__(cls)
        obj.y = 1000 + args[0] # args[0] is __init__(x)
        # when defined on instance, should not include `self`
        obj.f3 = lambda : obj.x + 30
        # when defined on class, must include `self`
        cls.f4 = lambda self: self.x + 40
        return obj
    
    
    def __init__(self, x):
        # self.y already exists BEFORE __init__ !
        assert hasattr(self, 'y') and self.y == 1000 + x
        print('MyClass.__init__: x=', x, 'y=', self.y)
        self.x = x
        # when defined on instance, should not include `self`
        self.f5 = lambda : self.x + 50
    
    def f1(self):
        return self.x + 10

    def f2(self):
        return self.x + 20
    
    def my_after_call(self):
        print('MyClass.my_after_call: x=', self.x, 'y=', self.y)


print('----- begin instantiation -----')
assert MyClass.__name__ == 'MyClassAmended'
obj = MyClass(6)
assert obj.f1() == 16
assert obj.f2() == 26
assert obj.f3() == 36
assert obj.f4() == 46
assert obj.f5() == 56
assert obj.g1() == -60
assert not hasattr(obj, 'g2')
assert obj.g3() == -180
assert obj.y == 1000 + 6

obj2 = MyClass(8)
assert obj2.y == 1000 + 8