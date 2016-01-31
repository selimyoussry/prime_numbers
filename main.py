import copy


class Prime:

    def __init__(self, maxi, sieve=True, prime_decomp=True):
        """
        :param maxi: the maximum of our exploration range
        :param sieve: perform the Sieve of Eratosthenes on load

        primes: dict, value = True iff key is prime
        prime_divisors: dict, list of prime divisors and their multiplicities for each number in the range
        """
        self.maxi = int(maxi)

        self.my_range = range(2, self.maxi + 1)
        self.primes = dict(
            zip(
                self.my_range,
                [True] * self.maxi
            )
        )

        # For each number in our range, the list of prime divisors with their multiplicities
        self.prime_divisors = dict(
            zip(
                self.my_range,
                [Divisors(n) for n in self.my_range]
            )
        )

        # Yields true iff the sieve has been performed until maxi
        self._sieved = False
        self._decomposed = False

        if sieve:
            self.sieve()

        if self._sieved and prime_decomp:
            self.get_prime_decomposition()

    def sieve(self, start_with=2):
        """
        Compute the Sieve of Eratosthenes and record the numbers' divisors
        """

        prime = start_with
        while prime < self.maxi:
            self.prime_divisors[prime].has_been_decomposed(yes=True)
            for alpha in range(2, self.maxi / prime + 1):
                n = alpha * prime
                self.primes[n] = False
                if not self.prime_divisors[n].has_been_decomposed():
                    self.prime_divisors[n].add_divisor(prime)
                    self.prime_divisors[n].add_divisor(alpha)
                    self.prime_divisors[n].has_been_decomposed(yes=True)

            # Get the new prime number
            prime += 1
            while prime < self.maxi and not self.primes[prime]:
                prime += 1

        self._sieved = True

    def get_primes(self):
        """
        :return: an ascending list of all the prime numbers until self.maxi
        """
        assert self._sieved
        return sorted([k for k, b in self.primes.iteritems() if b])

    def get_prime_decomposition(self):
        assert self._sieved
        for n in self.my_range:
            if not self.prime_divisors[n].is_complete(self.primes):

                to_add = []
                to_del = []
                for divisor, multiplicity in self.prime_divisors[n].divisors.iteritems():
                    if not self.primes[divisor]:
                        to_add.append((self.prime_divisors[divisor], multiplicity))
                        to_del.append(divisor)

                for q, m in to_add:
                    self.prime_divisors[n].add_divisors_of(q=q,m=m)

                for d in to_del:
                    self.prime_divisors[n].remove_divisor(d)

                self.prime_divisors[n].is_complete(yes=True)
        self._decomposed = True

    def _verify(self):
        assert self._sieved and self._decomposed
        check_product = dict()
        check_primes = dict()
        for number, divisors in self.prime_divisors.iteritems():
            check_product[number] = number == divisors.get_divisors_product() or self.primes[number]
            check_primes[number] = sum([self.primes[d] for d in divisors.divisors]) == len(divisors.divisors)
        for number in check_product:
            if not check_product[number]:
                print 'Problem with number {} - its divisors do not multiply to its value'.format(number)
            if not check_primes[number]:
                print 'Problem with {} - its divisors are not all prime numbers'.format(number)

class Divisors:

    def __init__(self, n):
        """
        :type n: int
        """
        self.n = n
        self.divisors = dict()
        self._is_complete = False
        self._has_been_decomposed = False

    def add_divisor(self, d, m=1):
        """
        :param d: divisor of self.n
        :type d: int
        :param m: multiplicity m
        :type m: int
        """
        self.divisors[d] = self.divisors[d] + m if d in self.divisors else m

    def remove_divisor(self, d, m=0):
        """
        :param d: divisor of self.n
        :type d: int
        :param m: multiplicity m
        :type m: int

        Removes the divisor d from the list, or decreases its multiplicity
        """
        assert d in self.divisors
        if m == 0 or self.divisors[d] == m:
            del self.divisors[d]
        else:
            self.divisors[d] -= m

    def add_divisors_of(self, q, m=1):
        """
        :type q: Divisors
        """
        assert q._is_complete
        for prime_divisor, multiplicity in q.divisors.iteritems():
            self.add_divisor(
                d=prime_divisor,
                m=multiplicity * m
            )

    def is_complete(self, primes=dict(), yes=False):
        """
        :type primes: dict
        :return:
        """
        if yes:
            self._is_complete = True

        if not self._is_complete:
            for divisor in self.divisors:
                if not primes[divisor]:
                    self._is_complete = False
                    return False
            self._is_complete = True
        return self._is_complete

    def get_divisors_product(self):
        product = 1
        for divisor, multiplicity in self.divisors.iteritems():
            product *= pow(divisor, multiplicity)
        return product

    def has_been_decomposed(self, yes=False):
        if yes:
            self._has_been_decomposed = True

        if not self._has_been_decomposed:
            self._has_been_decomposed = self.get_divisors_product() == self.n

        return self._has_been_decomposed

    def count_all_divisors(self):
        assert self._has_been_decomposed

        if self.n == 1:
            ret = 1
        elif len(self.divisors) == 0:
            ret = 2
        else:
            product = 1
            for d, m in self.divisors.iteritems():
                product *= (m + 1)
            ret = product

        return ret

    def get_all_divisors(self, sort=True):
        assert self._has_been_decomposed

        print 'sstr'

        if self.n == 1:
            ret = [1]
        elif len(self.divisors) == 0:
            ret = [1, self.n]
        else:
            ret = [1]
            for d, m in self.divisors.iteritems():
                cp_ret = copy.copy(ret)
                for mm in range(1, m + 1):
                    for k in cp_ret:
                        ret.append(pow(d, mm) * k)

        if sort:
            ret = sorted(ret)
        return ret
