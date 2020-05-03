from copy import deepcopy
from typing import Any, List, Tuple, Type


class Expression:
    label: str
    description: str

    def __repr__(self):
        return type(self).__name__

    @classmethod
    def resolve(self, prop, val):
        raise NotImplementedError("Should override this method in subclass")


class Gt(Expression):
    label = 'gt'
    description = 'Greater than'

    @classmethod
    def resolve(self, prop, val):
        return prop > val


class Gte(Expression):
    label = 'gte'
    description = 'Greater than or equal to'

    @classmethod
    def resolve(self, prop, val):
        return prop >= val


class Lt(Expression):
    label = 'lt'
    description = 'Lower than'

    @classmethod
    def resolve(self, prop, val):
        return prop < val


class Lte(Expression):
    label = 'lte'
    description = 'Lower than or equal to'

    @classmethod
    def resolve(self, prop, val):
        return prop <= val


class Equal(Expression):
    label = 'eq'
    description = 'Equal to'

    @classmethod
    def resolve(self, prop, val):
        return prop == val


class Is(Expression):
    label = 'is'
    description = 'is'

    @classmethod
    def resolve(self, prop, val):
        return prop is val


class Always(Expression):
    label = 'always'
    description = 'Always'

    @classmethod
    def resolve(self, prop, val):
        return True


class Never(Expression):
    label = 'never'
    description = 'Never'

    @classmethod
    def resolve(self, prop, val):
        return False


class And(Expression):
    label = 'And'
    description = 'And'

    @classmethod
    def resolve(self, prop, val):
        return prop and val


class Or(Expression):
    label = 'Or'
    description = 'Or'

    @classmethod
    def resolve(self, prop, val):
        return prop or val


class Not(Expression):
    label = 'Not'
    description = 'Not'

    @classmethod
    def resolve(self, prop, val=None):
        return not prop


class Condition(object):
    """
    A condition
    This class is meant to be used in order to set a condition on an object

    The syntax for setting a condition is :
         - Condition({property}__{expression}=value)

    Where :
        - property is the property concerned by the condition
        - expression is one of the expressions registered in Condition class
    Example :
        here we set a condition on property 'height' that check if height is greater or equal to 500px :
            >>> Condition(height__gte=500)
        here we want to check if name is equal to 'kiss' :
            >>> Condition(name='kiss')
    """

    # Conditions' expressions
    _expressions = {
        Gt.label: Gt,
        Gte.label: Gte,
        Lt.label: Lt,
        Lte.label: Lte,
        Equal.label: Equal,
        Is.label: Is,
        Always.label: Always,
        Never.label: Never,
    }

    def __init__(self, const: Any = None, **kwargs):
        # attributes
        self._expr = None
        self._prop = None
        self._val = None

        # Complements conditions
        self._complements = []  # type: List[Tuple[Type[Expression], Condition]]
        self._right = True

        if const is not None:
            if const:
                self._expr = Always
                self._prop = Always.label
            else:
                self._expr = Never
                self._prop = Never.label
            return

        if not len(kwargs) == 1:
            raise ValueError("Must give only expression for a condition")

        for k, v in kwargs.items():

            prop = k.split('__')

            if len(prop) > 2:
                raise ValueError("argument of expression should not have two(2) '__'")

            if not len(prop) > 1:
                expr = 'eq'
            else:
                expr = prop[-1]

            if not expr in self._expressions:
                raise ValueError(
                    f"'{expr}' is not a registered expression, must be one of {list(self._expressions.keys())}")

            self._expr = self._expressions[expr]
            self._prop = prop[0]
            self._val = v

    @property
    def prop(self):
        return self._prop

    @property
    def expression(self):
        if self._expr is Always:
            return Always.description
        elif self._expr is Never:
            return Never.description

        expr = f"{self._prop} {self._expressions[self._expr.label].description} {self._val}"
        if len(self._complements) > 0:
            for e, c in self.complements:
                expr = f"({expr}) {e.description} ({c.expression})"

        if not self._right:
            expr = f"Not ({expr})"

        return expr

    def __repr__(self):
        if self._expr is Always:
            return 'Condition(Always)'
        elif self._expr is Never:
            return 'Condition(Never)'

        repr_ = f"Condition({self._prop}{'' if self._expr == Equal else '__' + self._expr.label}={self._val})"
        if len(self._complements) > 0:
            for e, c in self.complements:
                repr_ = f"{repr_} {e.label} {c}"

        if not self._right:
            repr_ = f"Not ({repr_})"

        return repr_

    @property
    def complements(self):
        return sorted(
            self._complements, key=lambda cp: cp[0] != And
        )

    def resolve(self, for_: Any) -> bool:
        """
        Resolve if this condition is true for the object
        """
        if self._expr is Always:
            return True
        elif self._expr is Never:
            return False

        key = getattr(for_, self._prop)
        val = self._expressions[self._expr.label].resolve(key, self._val)

        for e, c in self.complements:
            val = e.resolve(c.resolve(for_), val)

        if not self._right:
            val = not val
        return val

    def __and__(self, other: 'Condition'):
        new = deepcopy(self)
        new._complements.append((And, other))
        return new

    def __or__(self, other: 'Condition'):
        new = deepcopy(self)
        new._complements.append((Or, other))
        return new

    def __invert__(self):
        new = deepcopy(self)
        new._right = not self._right
        return new


C = Condition

if __name__ == '__main__':
    c = C(is_running=True)
    c2 = C(x__gte=1)
    c3 = C(height=500)
    c4 = C(value__is=None)
    c5 = C(False)
    c6 = C(True)


    class Image:
        height = 500
        value = None
        x = -1

    #
    # print(c3, c3.expression)
    # print(c4, c4.expression)
    # print(c5, c5.expression)
    # print(c6, c6.expression)
    # print(c3.resolve(Image()))
    # print(c4.resolve(Image()))
    # print(c5.resolve(Image()))
    # print(c6.resolve(Image()))

    cc = c2 & c3
    print(cc)
    print(cc.expression)
    print(cc.resolve(Image()))


