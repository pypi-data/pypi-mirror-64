from math import gcd

from .variables import VariablesDict


class Monomial:
    """
    A Monomial is the product of a coefficient and
    some variables.

    Monomials can be added, subtracted, multiplied
    and divided togheter (and with numbers).
    lcm and gcd between monomials (and numbers) is
    available, too.

    You can also assign a value to the variables and
    calculate the value of that monomial with the
    value you assigned.
    """

    def __init__(self, coefficient=1, variables=VariablesDict(), **kwargs):
        """
        Creates a new Monomial.
        The default `coefficient` value is 1 (so it can be omitted);
        variables instead are empty for default

        >>> Monomial(17, k=3)
        17k**3
        >>> Monomial()
        1

        If `coefficient` is an instance of float but
        it's a whole number (like 18.0), it will be
        transformed in int (in this case, 18)

        >>> Monomial(7.0, a=2)
        7a**2

        Monomials can also be initialized by passing a dictionary
        (or anything similar) where are stored the variables:

        >>> Monomial(2, {'x': 2, 'y': 1})
        2x**2y

        Variables will be stored in a `VariableDict`.
        For more infos, see :func:`VariablesDict.__init__()`.)

        Once initialized the monomial, it
        calculates the monomial's total degree
        (which is the sum of the variables' degrees)

        >>> Monomial(-2, a=2, b=1, c=3).degree
        6

        :type coefficient: int, float
        :type coefficient: dict, VariablesDict
        :raise: ValueError, TypeError
        """

        # adjust arguments' order
        if isinstance(coefficient, dict) and not variables:
            variables = coefficient
            coefficient = 1
        elif not variables:
            variables = kwargs

        # Check the coefficient
        if isinstance(coefficient, float) and coefficient.is_integer():
            self.coefficient = int(coefficient)
        elif isinstance(coefficient, (int, float)):
            self.coefficient = coefficient
        else:
            raise TypeError("Coefficient must be int or float")

        # Check the variables
        self.variables = VariablesDict(variables)

        # Calculate the degree
        self.degree = sum(self.variables.values())

    ### Utility Methods ###

    def similar_to(self, other):
        """
        Checks if two monomials are similar (if
        the have the same variables).

        >>> m = Monomial(3, x=1, y=1)
        >>> m.similar_to(Monomial(3.14))
        False
        >>> m.similar_to(Monomial(2, x=1, y=1))
        True

        If the second operand is not a monomial
        the result will always be `False`

        >>> m.similar_to("")
        False

        When a monomial has no variables, if
        compared to a number the result will be `True`

        >>> Monomial(6).similar_to(6.28)
        True

        :type other: Monomial, int, float
        :rtype: bool
        """

        if self.variables.is_empty and isinstance(other, (int, float)):
            return True
        elif not isinstance(other, Monomial):
            return False

        return self.variables == other.variables

    def has_root(self, index):
        """
        Checks if the monomial "has" the root:
        the monomial `4x**2`, for example, is a square,
        so we can say it has root 2, because `(4x**2)**(1/2)`
        is a monomial (`2x`).

        >>> Monomial(4, x=2).has_root(2)
        True

        We can't say the same thing for `16a**4b`:

        >>> Monomial(16, a=4, b=1).has_root(2)
        False

        Zero has all the roots

        >>> Monomial(0).has_root(700)
        True

        :raises: TypeError
        :type index: int
        :rtype: bool
        """

        # check if index is int
        if not isinstance(index, int):
            raise TypeError(f"root index must be int, not {index.__class__.__name__}")

        # return always true if the coefficient is 0
        elif not self.coefficient:
            return True

        # return always false if index is even and
        # coefficient is negative
        elif not index % 2 and self.coefficient < 0:
            return False

        # try to apply the root to the index
        coefficient = abs(self.coefficient) ** (1/index)

        return coefficient.is_integer() and self.variables % index

    def root(self, index):
        """
        Calculates the root of given index of the monomial

        >>> Monomial(4, x=2).root(2)
        2x
        >>> Monomial(-27, a=9).root(3)
        -3a**3
        >>> Monomial(0).root(700)
        0

        If a monomial hasn't a root, it raises a `ValueError`

        >>> Monomial(5, b=2).root(3)
        Traceback (most recent call last):
        ...
        ValueError: this monomial hasn't root 3

        To see if a monomial has a root, use :func:`Monomial.has_root()`.

        :raises: ValueError
        :rtype: Monomial
        """

        # check if the monomial has the root
        if not self.has_root(index):
            raise ValueError(f"this monomial hasn't root {index}")

        # apply the root
        coefficient = abs(self.coefficient) ** (1/index)
        variables = self.variables / index

        # check if the coefficient is negative
        if self.coefficient < 0:
            coefficient = -coefficient

        return Monomial(coefficient, variables)

    def gcd(self, other):
        """
        Calculates the greatest common divisor of two
        monomials or numbers

        >>> a = Monomial(5, x=1, y=1)
        >>> b = Monomial(15, x=1)
        >>> a.gcd(b)
        5x

        It works only with integer coefficient/numbers
        different from zero

        >>> a.gcd(3.14)
        Traceback (most recent call last):
        ...
        TypeError: Can't calculate gcd between Monomial and float
        >>> a.gcd(Monomial(3.14))
        Traceback (most recent call last):
        ...
        ValueError: Monomial coefficient must be int
        >>> b.gcd(0)
        Traceback (most recent call last):
        ...
        ValueError: Coefficient can't be zero

        The result is always positive

        >>> c = Monomial(-30, x=1, y=1)
        >>> b.gcd(c)
        15x

        If you want to calculate the gcd with more
        factors, you can use the shorthand :func:`gcd`.

        :type others: Monomial, int, float
        :rtype: Monomial, int
        :raise: TypeError, ValueError
        """

        # Check types of the operators
        if isinstance(other, int):
            other = Monomial(other)
        elif isinstance(other, Monomial):
            if any(isinstance(m.coefficient, float) for m in [self, other]):
                raise ValueError("Monomial coefficient must be int")
        else:
            raise TypeError("Can't calculate gcd between Monomial"
                            f" and {type(other).__name__}")

        # Check value of the operators
        if self.coefficient == 0 or other.coefficient == 0:
            raise ValueError("Coefficient can't be zero")

        # Calculate the gcd of the coefficients
        coefficient = int(gcd(self.coefficient, other.coefficient))

        # Calculate the gcd of the variables
        variables = {}
        for variable in self.variables:
            if variable in other.variables:
                variables[variable] = min(self.variables[variable],
                                          other.variables[variable])

        return Monomial(coefficient, variables)

    def lcm(self, other):
        """
        Calculates the least common multiple of two monomials or numbers

        >>> a = Monomial(2, x=1, y=1)
        >>> b = Monomial(-9, y=3)
        >>> a.lcm(b)
        18xy**3

        If you want to know others informations
        like errors and limits, please check the
        documentation of Monomial().gcd().

        If you want to calculate the lcm between more
        monomials, you can use the :func:`lcm` shorthand.

        :type others: Monomial, int, float
        :rtype: Monomial, int, float
        :raise: TypeError, ValueError
        """

        return abs(self * other) / self.gcd(other)

    def eval(self, values=VariablesDict(), **kwargs):
        """
        Evaluates the monomial, giving values
        for each variable

        >>> m = Monomial(5, x=1, y=1)
        >>> m.eval(x=2, y=3)
        30

        **NB:** *if there are no variables left,
        it returns only the coefficient, as instance
        of `int` or `float`*

        You can also assign variables' values
        with a dictionary (or any subclass)

        >>> m.eval({'x': 2, 'y': 3})
        30

        If you omit some variables' values,
        those variables will remain as they
        were

        >>> m.eval(x=2)
        10y

        You can declare some variables values
        which aren't in the monomial and the
        result won't change

        >>> m.eval(b=7)
        5xy

        :type values: int, float, Monomial
        :rtype: int, float, Monomial
        :raise: TypeError
        """

        # use multiple initializations
        if not values:
            values = kwargs

        # lowerize the variables and prepare the result
        values = {v.lower(): values[v] for v in values}
        result = Monomial(self.coefficient, self.variables)

        # for every variable that is in the result
        for variable in values:
            if variable in result.variables:
                # multiply the result for the value
                # raised to the exponent. then divide for
                # the variable
                exp = result.variables[variable.lower()]
                result *= (values[variable] ** exp)
                result /= Monomial({variable: exp})

        # If there are no variables, return only the coefficient
        if result.variables.is_empty:
            return result.coefficient

        return result

    ### Operations Methods ###

    def __add__(self, other):
        """
        Sums two monomials.

        >>> Monomial(5, x=1, y=3) + Monomial(-1.52, x=1, y=3)
        3.48xy**3

        You can also sum a monomial and a number, but the
        result will be an instance of `Polynomial`.

        >>> Monomial(1, z=1) + 17
        z + 17

        :type other: Monomial, Polynomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        from . import Polynomial

        if isinstance(other, Monomial):
            # Opposite monomial
            if self == -other:
                return Monomial(0)

            # Simil monomial
            elif self.similar_to(other):
                return Monomial(self.coefficient + other.coefficient, self.variables)

            # Generic monomial
            else:
                return Polynomial(self, other)

        elif isinstance(other, (int, float)):
            if self.variables.is_empty:
                return Monomial(self.coefficient + other)

            else:
                return Polynomial(self, other)

        elif isinstance(other, Polynomial):
            return other + self

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Monomial' and '{other.__class__.__name__}'")

    def __sub__(self, other):
        """
        Returns the subtraction between this monomial
        and `other`

        >>> Monomial(5, x=1) - Monomial(3, x=1)
        2x

        If the monomials are not similar or the second
        operator is a number, the result will be a
        polynomial

        >>> Monomial(5, x=1, y=3) - Monomial(3, x=1)
        5xy**3 - 3x
        >>> Monomial(17, a=1, b=1) - 2.5
        17ab - 2.5

        :type other: Polynomial, Monomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        from . import Polynomial

        if isinstance(other, (Polynomial, Monomial, int, float)):
            return self + (-other)

        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Monomial' and '{other.__class__.__name__}'")

    def __mul__(self, other):
        """
        Multiplicates this monomial by `other`,
        which can be a monomial or a number

        >>> Monomial(5, x=1, y=2) * Monomial(2, a=1, b=1)
        10abxy**2
        >>> Monomial(3, c=2) * 5
        15c**2
        >>> Monomial(k=3) * Monomial(k=3)
        k**6

        :type other: Polynomial, Monomial, int, float
        :rtype: Polynomial, Monomial
        :raise: TypeError
        """

        from . import Polynomial

        # numbers
        if isinstance(other, (int, float)):
            other = Monomial(other)

        # monomials
        if isinstance(other, Monomial):
            coefficient = self.coefficient * other.coefficient
            variables = self.variables + other.variables

            return Monomial(coefficient, variables)

        # polynomials
        elif isinstance(other, Polynomial):
            return other * self

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Monomial' and '{other.__class__.__name__}'")

    def __truediv__(self, other):
        """
        Divide this monomial by another monomial or
        a number

        >>> Monomial(6, a=3) / Monomial(3, a=1)
        2a**2
        >>> Monomial(18, k=3) / 6
        3k**3
        >>> Monomial(27, x=6) / Monomial(3, x=6)
        9

        If `other`'s variable's exponents
        are higher than this monomial's, it raises a
        `ValueError`

        >>> Monomial(5) / Monomial(4, x=1)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be positive

        :type other: Monomial, int, float
        :rtype: Monomial
        :raise: ValueError, TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other)

        if isinstance(other, Monomial):
            coefficient = self.coefficient / other.coefficient
            variables = self.variables - other.variables
            return Monomial(coefficient, variables)

        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Monomial' and '{other.__class__.__name__}'")

    def __pow__(self, exp):
        """
        Raises a monomial to a given power

        >>> Monomial(5, x=1) ** 2
        25x**2
        >>> Monomial(4, c=6) ** 3
        64c**18

        If the exponent is 0, the result will be 1

        >>> Monomial(5, k=6) ** 0
        1

        It raises a `TypeError` if `exp` is an istance of `float`.

        >>> Monomial(3.14, a=3) ** 2.5
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Monomial' and 'float'

        It raises a `ValueError` if the exponent is negative

        >>> Monomial(17, k=1) ** (-1)
        Traceback (most recent call last):
        ...
        ValueError: Exponent can't be negative

        :type exp: int
        :rtype: Monomial
        :raise: ValueError, TypeError
        """

        # if the exponent is not an integer raise a typeerror
        if not isinstance(exp, int):
            raise TypeError(f"unsupported operand type(s) for ** or pow(): 'Monomial' and '{exp.__class__.__name__}'")

        # return 1 if the exponent is 0
        elif exp == 0:
            return 1

        # Raise an error if exponent is negative
        elif not exp > 0:
            raise ValueError("Exponent can't be negative")

        return Monomial(self.coefficient ** exp, self.variables * exp)

    ### Reversed Operations Method ###

    def __radd__(self, other):
        """
        This method is the reverse for :func:`Monomial.__add__`.
        With this method, you can swap the two operands
        of the addition:

        >>> 18 + Monomial(3)
        21

        For more informations, see :func:`Monomial.__add__` docs.

        :type other: Polynomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        try:
            return self + other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for +: '{other.__class__.__name__}' and 'Monomial'")

    def __rsub__(self, other):
        """
        This method is the reverse for :func:`Monomial.__sub__`.
        With this method, you can swap the two operands
        of the subtraction:

        >>> 9 - Monomial(4)
        5

        For more informations, see :func:`Monomial.__sub__` docs.

        :type other: Polynomial, int, float
        :rtype: Polynomial, Monomial, int, float
        :raise: TypeError
        """

        try:
            return (- self) + other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for -: '{other.__class__.__name__}' and 'Monomial'")

    def __rmul__(self, other):
        """
        This method is the reverse for :func:`Monomial.__mul__`.
        With this method, you can swap the two operands
        of the multiplication:

        >>> 5 * Monomial(2, x=2)
        10x**2

        For more informations, see :func:`Monomial.__mul__` docs.

        :type other: Polynomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        try:
            return self * other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for *: '{other.__class__.__name__}' and 'Monomial'")

    def __rtruediv__(self, other):
        """
        This method is the reverse for :func:`Monomial.__truediv__`.
        With this method, you can swap the two operands
        of the division:

        >>> 8 / Monomial(4)
        2

        For more informations, see :func:`Monomial.__truediv__ docs`.

        :type other: int, float
        :rtype: Monomial
        :raise: ValueError, TypeError
        """

        if not isinstance(other, (int, float)):
            raise TypeError(f"unsupported operand type(s) for /: '{other.__class__.__name__}' and 'Monomial'")

        if self.variables:
            raise ValueError("Exponent must be positive")

        return Monomial(other/self.coefficient)

    ### Magic Methods ###

    def __str__(self):
        """
        Returns the monomial as a string.
        Normally, it will return the coefficient and
        the variables without spaces or *.

        The power is indicated with **.

        Examples:
        >>> str(Monomial(5, x=1, y=1))
        '5xy'
        >>> str(Monomial(a=2))
        'a**2'
        >>> str(Monomial(-1, k=3))
        '-k**3'
        >>> str(Monomial(0, s=5))
        '0'
        >>> str(Monomial())
        '1'
        >>> str(Monomial(-1))
        '-1'

        Variables are displayed in alphabetical order

        >>> str(Monomial(5, k=2, b=3))
        '5b**3k**2'

        :rtype: str
        """

        variables = ""

        # order the variables
        for letter in sorted(self.variables.keys()):
            if self.variables[letter] > 1:
                variables += f"{letter}**{self.variables[letter]}"
            else:
                variables += letter

        # coefficient == 1 w/ variables
        if self.coefficient == 1 and variables:
            return variables

        # coefficient == -1 and w/ variables
        elif self.coefficient == -1 and self.variables:
            return '-' + variables

        # coefficient == 0
        elif self.coefficient == 0:
            return '0'

        # coefficient == 1 w/o variables
        elif self.coefficient == 1 and not self.variables:
            return '1'

        # coefficient == -1 w/o variables
        elif self.coefficient == -1 and not self.variables:
            return '-1'

        # normal monomial
        else:
            return str(self.coefficient) + variables

    def __repr__(self):
        """
        Returns the monomial as a string

        >>> Monomial(5, x=5)
        5x**5
        >>> Monomial(-1, a=2, c=3)
        -a**2c**3

        For more informations, see :func:Monomial.__str__()`.

        :rtype: str
        """

        return self.__str__()

    def __eq__(self, other):
        """
        Checks if two monomials are equivalent,
        comparing coefficients and variables

        >>> Monomial(5, x=1) == Monomial(5, x=1)
        True

        If there are no variables, it can be
        compared also to a number

        >>> Monomial(4) == 4
        True

        If the second operator isn't a monomial or
        a number, it will return `False`.

        :type other: Monomial, int, float
        :rtype: bool
        :raise: TypeError
        """

        try:
            return hash(self) == hash(other)
        except TypeError:
            return False

    def __neg__(self):
        """
        Returns the opposite of the monomial
        inverting the coefficient

        >>> - Monomial(5, x=1, y=1)
        -5xy

        :rtype: Monomial
        """
        return Monomial(-self.coefficient, self.variables)

    def __abs__(self):
        """
        Returns the absolute value of the monomial,
        calculating the absolute value of the coefficient

        >>> abs(Monomial(-3, a=1, b=4))
        3ab**4

        :rtype: Monomial
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __hash__(self):
        """
        Return the hash for the Monomial

        The hash for `8xy`, for example, is equivalent
        to the hash of `(8, ('x', 1), ('y', 1))`.

        >>> hash(Monomial(8, x=1, y=1)) == hash((8, ('x', 1), ('y', 1)))
        True

        If the monomial has no variables, its hash
        will be equal to the coefficient's hash

        >>> hash(Monomial(3)) == hash(3)
        True

        :rtype: int
        """

        if self.variables.is_empty:
            return hash(self.coefficient)

        variables = ((k, self.variables[k]) for k in sorted(self.variables.keys()))

        return hash((self.coefficient, ) + tuple(list(variables)))

# Variables shorthands
def Variable(letter):
    return Monomial(1, {str(letter): 1})
